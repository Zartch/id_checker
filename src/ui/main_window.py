"""
Ventana principal de la aplicación ID Checker.
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from ..csv_parser import parse_csv, CSVValidationError
from ..comparator import compare_ids
from ..history_manager import (
    get_history_files,
    get_results_folder,
    save_result,
    read_history_file
)


class MainWindow:
    """Ventana principal de ID Checker."""

    WINDOW_TITLE = "ID Checker - Comparador de IDs"
    WINDOW_MIN_WIDTH = 900
    WINDOW_MIN_HEIGHT = 600

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(self.WINDOW_TITLE)
        self.root.minsize(self.WINDOW_MIN_WIDTH, self.WINDOW_MIN_HEIGHT)

        self.testing_file: Path | None = None
        self.target_file: Path | None = None

        self._setup_ui()
        self._refresh_history_list()

    def _setup_ui(self):
        """Configura todos los elementos de la interfaz."""
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=3)
        self.root.rowconfigure(0, weight=1)

        self._create_history_panel()
        self._create_main_panel()

    def _create_history_panel(self):
        """Crea el panel izquierdo con el historial."""
        history_frame = ttk.LabelFrame(self.root, text="Historial", padding=10)
        history_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        history_frame.columnconfigure(0, weight=1)
        history_frame.rowconfigure(1, weight=1)

        results_path = get_results_folder()
        path_label = ttk.Label(
            history_frame,
            text=f"Ruta: {results_path}",
            wraplength=200,
            font=("TkDefaultFont", 8)
        )
        path_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))

        list_frame = ttk.Frame(history_frame)
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.history_listbox = tk.Listbox(
            list_frame,
            yscrollcommand=scrollbar.set,
            font=("TkDefaultFont", 9)
        )
        self.history_listbox.grid(row=0, column=0, sticky="nsew")
        self.history_listbox.bind('<<ListboxSelect>>', self._on_history_select)

        scrollbar.config(command=self.history_listbox.yview)

        refresh_btn = ttk.Button(
            history_frame,
            text="Actualizar lista",
            command=self._refresh_history_list
        )
        refresh_btn.grid(row=2, column=0, sticky="ew", pady=(5, 0))

    def _create_main_panel(self):
        """Crea el panel principal con los uploads y resultados."""
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        self._create_file_selector(
            main_frame,
            "Archivo TESTING",
            0,
            self._select_testing_file
        )
        self.testing_label = ttk.Label(main_frame, text="Ningún archivo seleccionado")
        self.testing_label.grid(row=1, column=0, sticky="ew", padx=10)

        self._create_file_selector(
            main_frame,
            "Archivo TARGET",
            1,
            self._select_target_file
        )
        self.target_label = ttk.Label(main_frame, text="Ningún archivo seleccionado")
        self.target_label.grid(row=1, column=1, sticky="ew", padx=10)

        self.compare_btn = ttk.Button(
            main_frame,
            text="Comparar archivos",
            command=self._compare_files,
            state="disabled"
        )
        self.compare_btn.grid(row=1, column=0, columnspan=2, pady=15)

        results_frame = ttk.LabelFrame(main_frame, text="Resultados", padding=10)
        results_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=(10, 0))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)

        text_frame = ttk.Frame(results_frame)
        text_frame.grid(row=0, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        y_scrollbar = ttk.Scrollbar(text_frame)
        y_scrollbar.grid(row=0, column=1, sticky="ns")

        x_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal")
        x_scrollbar.grid(row=1, column=0, sticky="ew")

        self.results_text = tk.Text(
            text_frame,
            wrap="none",
            yscrollcommand=y_scrollbar.set,
            xscrollcommand=x_scrollbar.set,
            font=("Courier", 10),
            state="disabled"
        )
        self.results_text.grid(row=0, column=0, sticky="nsew")

        y_scrollbar.config(command=self.results_text.yview)
        x_scrollbar.config(command=self.results_text.xview)

    def _create_file_selector(
        self,
        parent: ttk.Frame,
        label_text: str,
        column: int,
        command
    ):
        """Crea un selector de archivo con etiqueta y botón."""
        frame = ttk.Frame(parent)
        frame.grid(row=0, column=column, sticky="ew", padx=10, pady=10)
        frame.columnconfigure(0, weight=1)

        label = ttk.Label(frame, text=label_text, font=("TkDefaultFont", 11, "bold"))
        label.grid(row=0, column=0, pady=(0, 5))

        btn = ttk.Button(frame, text="Seleccionar CSV", command=command)
        btn.grid(row=1, column=0)

    def _select_testing_file(self):
        """Abre diálogo para seleccionar archivo Testing."""
        filepath = self._open_file_dialog()
        if filepath:
            self.testing_file = filepath
            self.testing_label.config(text=filepath.name)
            self._update_compare_button_state()

    def _select_target_file(self):
        """Abre diálogo para seleccionar archivo Target."""
        filepath = self._open_file_dialog()
        if filepath:
            self.target_file = filepath
            self.target_label.config(text=filepath.name)
            self._update_compare_button_state()

    def _open_file_dialog(self) -> Path | None:
        """Abre diálogo de selección de archivo CSV."""
        filepath = filedialog.askopenfilename(
            title="Seleccionar archivo CSV",
            filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")]
        )
        return Path(filepath) if filepath else None

    def _update_compare_button_state(self):
        """Activa/desactiva el botón de comparar según los archivos seleccionados."""
        if self.testing_file and self.target_file:
            self.compare_btn.config(state="normal")
        else:
            self.compare_btn.config(state="disabled")

    def _compare_files(self):
        """Ejecuta la comparación de los archivos seleccionados."""
        if not self.testing_file or not self.target_file:
            return

        try:
            testing_result = parse_csv(self.testing_file)
            target_result = parse_csv(self.target_file)

            comparison = compare_ids(testing_result, target_result)
            saved_path = save_result(comparison)

            content = read_history_file(saved_path)
            self._show_results(content)
            self._refresh_history_list()

            messagebox.showinfo(
                "Comparación completada",
                f"Resultado guardado en:\n{saved_path}"
            )

        except CSVValidationError as e:
            messagebox.showerror("Error de validación", str(e))
        except FileNotFoundError as e:
            messagebox.showerror("Archivo no encontrado", str(e))
        except Exception as e:
            messagebox.showerror("Error inesperado", f"Ocurrió un error: {e}")

    def _show_results(self, content: str):
        """Muestra contenido en el área de resultados."""
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert("1.0", content)
        self.results_text.config(state="disabled")

    def _refresh_history_list(self):
        """Actualiza la lista de archivos históricos."""
        self.history_listbox.delete(0, tk.END)

        history_files = get_history_files()
        self._history_files = history_files

        for filepath in history_files:
            display_name = filepath.stem.replace("id_checker_diff_", "")
            self.history_listbox.insert(tk.END, display_name)

    def _on_history_select(self, event):
        """Maneja la selección de un archivo del historial."""
        selection = self.history_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if index < len(self._history_files):
            filepath = self._history_files[index]
            try:
                content = read_history_file(filepath)
                self._show_results(content)
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def run(self):
        """Inicia el loop principal de la aplicación."""
        self.root.mainloop()
