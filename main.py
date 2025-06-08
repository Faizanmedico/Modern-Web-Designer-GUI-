import tkinter as tk
from tkinter import filedialog, messagebox

class WebDesignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Web Designer")
        self.canvas = tk.Canvas(root, bg="white", height=600, width=800)
        self.canvas.pack(fill="both", expand=True)

        self.elements = []
        self.selected_element = None
        self.next_element_y = 30  # To avoid overlapping placed elements

        self.setup_toolbar()
        self.setup_right_click_menu()

    def setup_toolbar(self):
        toolbar = tk.Frame(self.root, bg="#f0f0f0", height=40)
        toolbar.pack(fill="x")

        tk.Button(toolbar, text="Add Header", command=lambda: self.add_element("header")).pack(side="left", padx=5, pady=5)
        tk.Button(toolbar, text="Add Paragraph", command=lambda: self.add_element("paragraph")).pack(side="left", padx=5)
        tk.Button(toolbar, text="Add Button", command=lambda: self.add_element("button")).pack(side="left", padx=5)
        tk.Button(toolbar, text="Add Image", command=lambda: self.add_element("image")).pack(side="left", padx=5)
        tk.Button(toolbar, text="Export HTML", command=self.export_html).pack(side="right", padx=10)

    def setup_right_click_menu(self):
        self.right_click_menu = tk.Menu(self.root, tearoff=0)
        self.right_click_menu.add_command(label="Edit Properties", command=lambda: self.show_properties(self.selected_element))
        self.right_click_menu.add_command(label="Delete", command=self.delete_selected_element)

    def add_element(self, type_):
        frame = tk.Frame(self.canvas, bd=1, relief="solid")
        content = {
            "header": "Header Text",
            "paragraph": "Paragraph text goes here.",
            "button": "Click Me",
            "image": "Image description"
        }[type_]

        widget = None
        if type_ == "header":
            widget = tk.Label(frame, text=content, font=("Arial", 24))
        elif type_ == "paragraph":
            widget = tk.Label(frame, text=content, font=("Arial", 14))
        elif type_ == "button":
            widget = tk.Button(frame, text=content)
        elif type_ == "image":
            widget = tk.Label(frame, text="[Image]", bg="gray", width=20, height=5)

        widget.pack(padx=10, pady=10)
        # Place each new window at a lower Y position to avoid overlap
        window = self.canvas.create_window(100, self.next_element_y, window=frame, anchor="nw")
        self.next_element_y += 80

        element = {
            "type": type_,
            "content": content,
            "frame": frame,
            "window": window,
            "styles": {
                "bg_color": "white",
                "text_color": "black",
                "padding": 10,
                "margin": 5,
                "border_radius": 0,
                "font_size": 24 if type_ == "header" else 14
            }
        }

        frame.bind("<Button-1>", lambda e, el=element: self.select_element(el))
        frame.bind("<Button-3>", lambda e, el=element: self.show_right_click_menu(e, el))

        self.elements.append(element)

    def select_element(self, element):
        self.selected_element = element

    def show_right_click_menu(self, event, element):
        self.select_element(element)
        self.right_click_menu.tk_popup(event.x_root, event.y_root)

    def delete_selected_element(self):
        if self.selected_element:
            self.canvas.delete(self.selected_element["window"])
            self.elements.remove(self.selected_element)
            self.selected_element = None

    def show_properties(self, element):
        if not element:
            return

        properties_window = tk.Toplevel(self.root)
        properties_window.title("Element Properties")

        tk.Label(properties_window, text="Content:").pack()
        content_entry = tk.Entry(properties_window)
        content_entry.insert(0, element['content'])
        content_entry.pack()

        tk.Label(properties_window, text="Background Color (hex):").pack()
        bg_entry = tk.Entry(properties_window)
        bg_entry.insert(0, element['styles'].get("bg_color", "white"))
        bg_entry.pack()

        tk.Label(properties_window, text="Text Color (hex):").pack()
        fg_entry = tk.Entry(properties_window)
        fg_entry.insert(0, element['styles'].get("text_color", "black"))
        fg_entry.pack()

        tk.Label(properties_window, text="Padding (px):").pack()
        padding_entry = tk.Entry(properties_window)
        padding_entry.insert(0, str(element['styles'].get("padding", 10)))
        padding_entry.pack()

        tk.Label(properties_window, text="Margin (px):").pack()
        margin_entry = tk.Entry(properties_window)
        margin_entry.insert(0, str(element['styles'].get("margin", 5)))
        margin_entry.pack()

        tk.Label(properties_window, text="Border Radius (px):").pack()
        radius_entry = tk.Entry(properties_window)
        radius_entry.insert(0, str(element['styles'].get("border_radius", 0)))
        radius_entry.pack()

        tk.Label(properties_window, text="Font Size (px):").pack()
        font_entry = tk.Entry(properties_window)
        font_entry.insert(0, str(element['styles'].get("font_size", 14)))
        font_entry.pack()

        def apply_properties():
            try:
                padding = int(padding_entry.get())
                margin = int(margin_entry.get())
                border_radius = int(radius_entry.get())
                font_size = int(font_entry.get())
            except ValueError:
                messagebox.showerror("Invalid input", "Padding, Margin, Border Radius, and Font Size must be integers.")
                return

            element['content'] = content_entry.get()
            element['styles'] = {
                "bg_color": bg_entry.get(),
                "text_color": fg_entry.get(),
                "padding": padding,
                "margin": margin,
                "border_radius": border_radius,
                "font_size": font_size
            }

            for widget in element['frame'].winfo_children():
                if isinstance(widget, tk.Label):
                    widget.config(
                        text=element['content'],
                        bg=element['styles']['bg_color'],
                        fg=element['styles']['text_color'],
                        font=("Arial", element['styles']['font_size']),
                        padx=element['styles']['padding'],
                        pady=element['styles']['padding']
                    )
                elif isinstance(widget, tk.Button):
                    widget.config(
                        text=element['content'],
                        bg=element['styles']['bg_color'],
                        fg=element['styles']['text_color'],
                        font=("Arial", element['styles']['font_size']),
                        padx=element['styles']['padding'],
                        pady=element['styles']['padding']
                    )
            properties_window.destroy()

        tk.Button(properties_window, text="Apply", command=apply_properties).pack(pady=10)

    def export_html(self):
        html = """<!DOCTYPE html>
<html>
<head>
<style>
body { font-family: Arial, sans-serif; }
</style>
</head>
<body>
"""

        for element in self.elements:
            styles = element.get("styles", {})
            style_str = (
                f"background-color: {styles.get('bg_color', '#ffffff')}; "
                f"color: {styles.get('text_color', '#000000')}; "
                f"padding: {styles.get('padding', 10)}px; "
                f"margin: {styles.get('margin', 5)}px; "
                f"border-radius: {styles.get('border_radius', 0)}px; "
                f"font-size: {styles.get('font_size', 14)}px; "
            )

            content = element['content']
            if element['type'] == 'header':
                html += f'<h1 style="{style_str}">{content}</h1>\n'
            elif element['type'] == 'paragraph':
                html += f'<p style="{style_str}">{content}</p>\n'
            elif element['type'] == 'button':
                html += f'<button style="{style_str}">{content}</button>\n'
            elif element['type'] == 'image':
                html += f'<img src="#" alt="{content}" style="{style_str} width:100%; height:auto;">\n'

        html += "</body>\n</html>"

        file_path = filedialog.asksaveasfilename(defaultextension=".html", filetypes=[("HTML files", "*.html")])
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(html)
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebDesignerApp(root)
    root.mainloop()