import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import webbrowser
import os

# Try to import ThemedStyle for better themes
try:
    from ttkthemes import ThemedStyle
except ImportError:
    ThemedStyle = None

class WebDesignApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Web Designer")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        
        # Configure theme colors
        self.bg_color = "#f5f5f5"
        self.sidebar_color = "#2c3e50"
        self.accent_color = "#3498db"
        self.text_color = "#333333"
        
        self.root.configure(bg=self.bg_color)
        
        # Create variables to store design elements
        self.current_project = None
        self.elements = []
        self.selected_element = None
        self.custom_styles = {}
        
        self.setup_ui()

    def setup_ui(self):
        # Configure grid layout
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        # Left Sidebar - Tools Panel
        self.sidebar = tk.Frame(self.root, bg=self.sidebar_color, width=200)
        self.sidebar.grid(row=0, column=0, sticky="nswe", padx=5, pady=5)
        
        # Main Content Area - Design Canvas
        self.canvas_frame = tk.Frame(self.root, bg="white", bd=2, relief=tk.GROOVE)
        self.canvas_frame.grid(row=0, column=1, sticky="nswe", padx=5, pady=5)
        
        # Right Panel - Properties Editor
        self.properties_panel = tk.Frame(self.root, bg=self.bg_color, width=300)
        self.properties_panel.grid(row=0, column=2, sticky="nswe", padx=5, pady=5)
        
        # Configure resizing
        self.canvas_frame.grid_propagate(False)
        self.sidebar.grid_propagate(False)
        self.properties_panel.grid_propagate(False)
        
        # Add components
        self.create_toolbox()
        self.create_properties_panel()
        self.create_menu()
        self.create_canvas()
        self.create_status_bar()

    def create_toolbox(self):
        # Toolbox header
        header = tk.Label(self.sidebar, text="ELEMENTS", bg=self.sidebar_color, 
                         fg="white", font=('Helvetica', 10, 'bold'))
        header.pack(fill="x", pady=(10,5), padx=5)
        
        # Element buttons
        elements = [
            ("Header", self.add_header),
            ("Paragraph", self.add_paragraph),
            ("Button", self.add_button),
            ("Image", self.add_image),
            ("Divider", self.add_divider),
            ("Form", self.add_form)
        ]
        
        for text, command in elements:
            btn = tk.Button(self.sidebar, text=text, bg=self.accent_color, fg="white",
                          relief=tk.FLAT, command=command)
            btn.pack(fill="x", pady=2, padx=5)
        
        # Style section
        style_header = tk.Label(self.sidebar, text="STYLES", bg=self.sidebar_color,
                               fg="white", font=('Helvetica', 10, 'bold'))
        style_header.pack(fill="x", pady=(20,5), padx=5)
        
        style_buttons = [
            ("Color Palette", self.open_color_picker),
            ("Font Settings", self.open_font_dialog),
            ("Layout Tools", self.open_layout_tools)
        ]
        
        for text, command in style_buttons:
            btn = tk.Button(self.sidebar, text=text, bg="#34495e", fg="white",
                          relief=tk.FLAT, command=command)
            btn.pack(fill="x", pady=2, padx=5)

    def create_canvas(self):
        # Canvas for web design preview
        self.design_canvas = tk.Canvas(self.canvas_frame, bg="white", bd=0,
                                      highlightthickness=0)
        self.design_canvas.pack(fill="both", expand=True)
        
        # Configure canvas scrolling
        self.scroll_y = ttk.Scrollbar(self.canvas_frame, orient="vertical", 
                                     command=self.design_canvas.yview)
        self.scroll_y.pack(side="right", fill="y")
        self.design_canvas.configure(yscrollcommand=self.scroll_y.set)
        
        # Frame inside canvas for elements
        self.elements_frame = tk.Frame(self.design_canvas, bg="white")
        self.canvas_window = self.design_canvas.create_window(
            (0, 0), window=self.elements_frame, anchor="nw")
        
        # Bind events
        self.elements_frame.bind("<Configure>", self.on_frame_configure)
        self.design_canvas.bind("<Configure>", self.on_canvas_configure)
        
    def on_frame_configure(self, event):
        self.design_canvas.configure(scrollregion=self.design_canvas.bbox("all"))
        
    def on_canvas_configure(self, event):
        self.design_canvas.itemconfig(self.canvas_window, width=event.width)

    def create_properties_panel(self):
        # Properties header
        header = tk.Label(self.properties_panel, text="PROPERTIES", bg=self.bg_color,
                         fg=self.text_color, font=('Helvetica', 10, 'bold'))
        header.pack(fill="x", pady=(10,5), padx=5)
        
        # Element properties frame
        self.element_properties = tk.Frame(self.properties_panel, bg=self.bg_color)
        self.element_properties.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Default empty state
        empty_label = tk.Label(self.element_properties, text="No element selected",
                             bg=self.bg_color, fg="#7f8c8d")
        empty_label.pack(pady=20)
        
        # Global styles section
        self.create_global_styles_section()
        
    def create_global_styles_section(self):
        styles_frame = tk.LabelFrame(self.properties_panel, text="Global Styles",
                                   bg=self.bg_color, fg=self.text_color)
        styles_frame.pack(fill="x", padx=5, pady=10)
        
        # Background color
        tk.Label(styles_frame, text="Background:", bg=self.bg_color).grid(row=0, column=0, sticky="w")
        self.bg_color_entry = tk.Entry(styles_frame, width=10)
        self.bg_color_entry.grid(row=0, column=1, sticky="w")
        self.bg_color_entry.insert(0, "#ffffff")
        
        # Font family
        tk.Label(styles_frame, text="Font Family:", bg=self.bg_color).grid(row=1, column=0, sticky="w")
        self.font_family_var = tk.StringVar(value="Arial")
        font_menu = ttk.Combobox(styles_frame, textvariable=self.font_family_var,
                               values=["Arial", "Helvetica", "Times New Roman", "Courier New"])
        font_menu.grid(row=1, column=1, sticky="we")
        
        # Apply button
        apply_btn = tk.Button(styles_frame, text="Apply Styles", command=self.apply_global_styles,
                            bg=self.accent_color, fg="white")
        apply_btn.grid(row=2, column=0, columnspan=2, pady=5, sticky="we")

    def add_header(self):
        element_id = f"header_{len(self.elements)}"
        header_frame = tk.Frame(self.elements_frame, bd=1, relief=tk.RIDGE, bg="white")
        header_frame.pack(fill="x", pady=5, padx=10)
        
        # Header content
        header_label = tk.Label(header_frame, text="New Header", font=('Helvetica', 18, 'bold'),
                              bg="white", fg="#333333")
        header_label.pack(pady=10, padx=10)
        
        # Store element data
        element_data = {
            "id": element_id,
            "type": "header",
            "frame": header_frame,
            "content": "New Header",
            "styles": {
                "font_size": 18,
                "font_weight": "bold",
                "color": "#333333",
                "alignment": "left"
            }
        }
        self.elements.append(element_data)
        
        # Make draggable and selectable
        self.make_draggable(header_frame, element_data)
        self.update_status("Header added.")
        
    def add_paragraph(self):
        element_id = f"paragraph_{len(self.elements)}"
        para_frame = tk.Frame(self.elements_frame, bd=1, relief=tk.RIDGE, bg="white")
        para_frame.pack(fill="x", pady=5, padx=10)
        
        # Paragraph content
        para_text = tk.Text(para_frame, height=3, wrap=tk.WORD, font=('Helvetica', 12),
                          bg="white", fg="#333333", padx=5, pady=5)
        para_text.insert(tk.END, "Lorem ipsum dolor sit amet, consectetur adipiscing elit.")
        para_text.pack(fill="x", padx=5, pady=5)
        
        # Store element data
        element_data = {
            "id": element_id,
            "type": "paragraph",
            "frame": para_frame,
            "content": "Lorem ipsum...",
            "styles": {
                "font_size": 12,
                "color": "#333333",
                "line_height": 1.5
            }
        }
        self.elements.append(element_data)
        
        # Make draggable and selectable
        self.make_draggable(para_frame, element_data)
        self.update_status("Paragraph added.")

    def add_button(self):
        element_id = f"button_{len(self.elements)}"
        button_frame = tk.Frame(self.elements_frame, bd=1, relief=tk.RIDGE, bg="white")
        button_frame.pack(fill="x", pady=5, padx=10)

        btn = tk.Button(button_frame, text="Click Me", bg=self.accent_color, fg="white",
                        relief=tk.FLAT, font=('Helvetica', 12, 'bold'))
        btn.pack(pady=10, padx=10)

        element_data = {
            "id": element_id,
            "type": "button",
            "frame": button_frame,
            "content": "Click Me",
            "styles": {
                "background_color": self.accent_color,
                "color": "white",
                "font_size": 12,
                "font_weight": "bold"
            }
        }
        self.elements.append(element_data)
        self.make_draggable(button_frame, element_data)
        self.update_status("Button added.")

    def add_image(self):
        element_id = f"image_{len(self.elements)}"
        image_frame = tk.Frame(self.elements_frame, bd=1, relief=tk.RIDGE, bg="white")
        image_frame.pack(fill="x", pady=5, padx=10)

        image_label = tk.Label(image_frame, text="[Image Placeholder]", bg="white", fg="#7f8c8d",
                               font=('Helvetica', 12))
        image_label.pack(pady=20, padx=20)

        element_data = {
            "id": element_id,
            "type": "image",
            "frame": image_frame,
            "content": "placeholder.png", # In a real app, this would be an image path
            "styles": {
                "width": "auto",
                "height": "auto"
            }
        }
        self.elements.append(element_data)
        self.make_draggable(image_frame, element_data)
        self.update_status("Image placeholder added.")

    def add_divider(self):
        element_id = f"divider_{len(self.elements)}"
        divider_frame = tk.Frame(self.elements_frame, bd=0, bg="white")
        divider_frame.pack(fill="x", pady=5, padx=10)

        divider_line = tk.Frame(divider_frame, height=2, bg="#cccccc", relief=tk.GROOVE)
        divider_line.pack(fill="x", pady=10)

        element_data = {
            "id": element_id,
            "type": "divider",
            "frame": divider_frame,
            "styles": {
                "height": 2,
                "color": "#cccccc"
            }
        }
        self.elements.append(element_data)
        self.make_draggable(divider_frame, element_data)
        self.update_status("Divider added.")

    def add_form(self):
        element_id = f"form_{len(self.elements)}"
        form_frame = tk.Frame(self.elements_frame, bd=1, relief=tk.RIDGE, bg="white")
        form_frame.pack(fill="x", pady=5, padx=10)

        tk.Label(form_frame, text="Contact Form", font=('Helvetica', 14, 'bold'), bg="white").pack(pady=5)
        tk.Label(form_frame, text="Name:", bg="white").pack(anchor="w", padx=10)
        tk.Entry(form_frame, width=40).pack(fill="x", padx=10, pady=2)
        tk.Label(form_frame, text="Email:", bg="white").pack(anchor="w", padx=10)
        tk.Entry(form_frame, width=40).pack(fill="x", padx=10, pady=2)
        tk.Label(form_frame, text="Message:", bg="white").pack(anchor="w", padx=10)
        tk.Text(form_frame, height=5, wrap=tk.WORD).pack(fill="x", padx=10, pady=2)
        tk.Button(form_frame, text="Submit", bg=self.accent_color, fg="white", relief=tk.FLAT).pack(pady=10)

        element_data = {
            "id": element_id,
            "type": "form",
            "frame": form_frame,
            "content": "Contact Form",
            "styles": {} # Styles would be more complex for a form
        }
        self.elements.append(element_data)
        self.make_draggable(form_frame, element_data)
        self.update_status("Form added.")


    def make_draggable(self, widget, element_data):
        widget.bind("<Button-1>", lambda e: self.select_element(element_data))
        widget.bind("<B1-Motion>", self.on_drag)
        
    def select_element(self, element_data):
        # Deselect previous element if any
        if self.selected_element and self.selected_element['frame']:
            self.selected_element['frame'].config(bd=1, relief=tk.RIDGE)
        
        self.selected_element = element_data
        # Highlight selected element
        if self.selected_element and self.selected_element['frame']:
            self.selected_element['frame'].config(bd=2, relief=tk.SOLID, highlightbackground=self.accent_color)
        
        self.update_properties_panel()
        self.update_status(f"Selected element: {element_data['type'].capitalize()}")
        
    def on_drag(self, event):
        # Simple drag implementation - in a real app you'd want to implement proper reordering
        # For a basic visual drag, you could lift the widget to the top
        if self.selected_element and self.selected_element['frame']:
            self.selected_element['frame'].lift()
        pass # Placeholder for more complex drag-and-drop logic


    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project", command=self.new_project)
        file_menu.add_command(label="Open Project", command=self.open_project)
        file_menu.add_command(label="Save Project", command=self.save_project)
        file_menu.add_separator()
        file_menu.add_command(label="Export HTML", command=self.export_html)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", command=self.undo_action)
        edit_menu.add_command(label="Redo", command=self.redo_action)
        edit_menu.add_separator()
        edit_menu.add_command(label="Preferences", command=self.open_preferences)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        view_menu.add_command(label="Preview in Browser", command=self.preview_in_browser)
        menubar.add_cascade(label="View", menu=view_menu)
        
        self.root.config(menu=menubar)

    def new_project(self):
        self.elements = []
        self.selected_element = None
        self.current_project = None
        
        # Clear canvas
        for widget in self.elements_frame.winfo_children():
            widget.destroy()
            
        self.update_status("New project created. Start adding elements!")
        
    def open_project(self):
        file_path = filedialog.askopenfilename(
            defaultextension=".wdp",
            filetypes=[("Web Design Projects", "*.wdp"), ("All Files", "*.*")])
        
        if file_path:
            self.current_project = file_path
            try:
                with open(file_path, 'r') as f:
                    # In a real application, you'd parse the saved data
                    # and reconstruct elements on the canvas.
                    # For now, let's just indicate it's opened.
                    content = f.read()
                    print(f"Opened project content:\n{content}") # For debugging
                self.update_status(f"Project '{os.path.basename(file_path)}' opened.")
                messagebox.showinfo("Success", "Project opened successfully! (Reconstruction not fully implemented yet)")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open project: {str(e)}")
            
    def save_project(self):
        if not self.current_project:
            self.save_project_as()
        else:
            self.save_to_file(self.current_project)
            
    def save_project_as(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".wdp",
            filetypes=[("Web Design Projects", "*.wdp"), ("All Files", "*.*")])
            
        if file_path:
            self.current_project = file_path
            self.save_to_file(file_path)
            
    def save_to_file(self, file_path):
        try:
            # In a real app, you would serialize all element data (type, content, styles, position)
            # A simple way for now is to save a representation of the elements list
            with open(file_path, 'w') as f:
                f.write("Web Design Project File\n")
                for element in self.elements:
                    f.write(f"Element: {element['type']}, Content: {element['content']}\n")
                
            messagebox.showinfo("Success", "Project saved successfully!")
            self.update_status(f"Project saved to {os.path.basename(file_path)}.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save project: {str(e)}")

    def undo_action(self):
        messagebox.showinfo("Undo", "Undo functionality not yet implemented.")
        self.update_status("Undo action.")

    def redo_action(self):
        messagebox.showinfo("Redo", "Redo functionality not yet implemented.")
        self.update_status("Redo action.")

    def open_preferences(self):
        messagebox.showinfo("Preferences", "Preferences dialog not yet implemented.")
        self.update_status("Opened preferences.")

    def open_color_picker(self):
        messagebox.showinfo("Color Picker", "Color picker dialog not yet implemented.")
        self.update_status("Opened color picker.")

    def open_font_dialog(self):
        messagebox.showinfo("Font Settings", "Font settings dialog not yet implemented.")
        self.update_status("Opened font settings.")

    def open_layout_tools(self):
        messagebox.showinfo("Layout Tools", "Layout tools dialog not yet implemented.")
        self.update_status("Opened layout tools.")

    def apply_global_styles(self):
        new_bg_color = self.bg_color_entry.get()
        new_font_family = self.font_family_var.get()

        self.elements_frame.config(bg=new_bg_color)
        # Apply font family to existing elements (simplified)
        for element in self.elements:
            if element['type'] in ['header', 'paragraph', 'button']:
                # This is a simplified application. In a real app, you'd access the specific
                # text widget or label and update its font.
                # For example, if header_label is accessible:
                # element['label_widget'].config(font=(new_font_family, element['styles']['font_size']))
                pass # More detailed implementation needed here

        self.update_status(f"Applied global styles: BG={new_bg_color}, Font={new_font_family}")
        messagebox.showinfo("Global Styles", "Global styles applied. (Note: Font application to existing elements is simplified)")

    def update_properties_panel(self):
        # Clear existing properties
        for widget in self.element_properties.winfo_children():
            widget.destroy()

        if self.selected_element:
            tk.Label(self.element_properties, text=f"Type: {self.selected_element['type'].capitalize()}",
                     bg=self.bg_color, fg=self.text_color, font=('Helvetica', 10, 'bold')).pack(pady=5)
            
            # Example: display content for editable elements
            if 'content' in self.selected_element:
                tk.Label(self.element_properties, text="Content:", bg=self.bg_color).pack(anchor="w")
                content_entry = tk.Entry(self.element_properties, width=30)
                content_entry.insert(0, self.selected_element['content'])
                content_entry.pack(fill="x", pady=2)
                
                # You'd add a command to update the element's content here
                # content_entry.bind("<Return>", lambda e: self.update_element_content(self.selected_element, content_entry.get()))

            # Example: display styles
            if 'styles' in self.selected_element:
                tk.Label(self.element_properties, text="Styles:", bg=self.bg_color, font=('Helvetica', 9, 'italic')).pack(anchor="w", pady=(10,0))
                for style_key, style_value in self.selected_element['styles'].items():
                    tk.Label(self.element_properties, text=f"  - {style_key}: {style_value}", bg=self.bg_color).pack(anchor="w")
            
            # Add more specific property controls based on element type
            # e.g., for 'header': font size, alignment, color pickers
            # e.g., for 'image': source path, width, height
        else:
            empty_label = tk.Label(self.element_properties, text="No element selected",
                                 bg=self.bg_color, fg="#7f8c8d")
            empty_label.pack(pady=20)


    def preview_in_browser(self):
        # Create temporary HTML file
        html_content = self.generate_html()
        temp_file = "preview.html"
        
        try:
            with open(temp_file, 'w') as f:
                f.write(html_content)
                
            # Open in default browser
            webbrowser.open(f"file://{os.path.abspath(temp_file)}")
            self.update_status("Preview opened in browser.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open preview: {str(e)}")
            self.update_status("Failed to open preview.")
        
    def export_html(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".html",
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")])
            
        if file_path:
            html_content = self.generate_html()
            
            try:
                with open(file_path, 'w') as f:
                    f.write(html_content)
                messagebox.showinfo("Success", "HTML exported successfully!")
                self.update_status(f"HTML exported to {os.path.basename(file_path)}.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export HTML: {str(e)}")
                self.update_status("Failed to export HTML.")
                
    def generate_html(self):
        # Basic HTML template
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>My Web Design</title>
    <style>
        body {{
            font-family: {self.font_family_var.get()}, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: {self.bg_color_entry.get()};
        }}
        .container {{
            max-width: 800px;
            margin: 0 auto;
        }}
        h1 {{
            color: #333333;
            font-size: 18px;
            font-weight: bold;
        }}
        p {{
            color: #333333;
            font-size: 12px;
            line-height: 1.5;
        }}
        button {{
            background-color: {self.accent_color};
            color: white;
            padding: 10px 15px;
            border: none;
            cursor: pointer;
            font-size: 12px;
            font-weight: bold;
        }}
        .image-placeholder {{
            width: 150px;
            height: 100px;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            border: 1px dashed #ccc;
            color: #7f8c8d;
            font-size: 12px;
        }}
        .divider {{
            height: 2px;
            background-color: #cccccc;
            margin: 20px 0;
        }}
        .form-container {{
            padding: 20px;
            border: 1px solid #eee;
            background-color: #f9f9f9;
        }}
        .form-container input[type="text"],
        .form-container input[type="email"],
        .form-container textarea {{
            width: calc(100% - 20px);
            padding: 8px;
            margin-bottom: 10px;
            border: 1px solid #ddd;
        }}
        .form-container button {{
            width: auto;
            padding: 8px 20px;
        }}
        </style>
        </head>
        <body>
        <div class="container">
"""
        
        # Add elements to HTML
        for element in self.elements:
            if element['type'] == 'header':
                # Apply styles from element_data if they exist and are relevant
                font_size = element['styles'].get('font_size', 18)
                font_weight = element['styles'].get('font_weight', 'bold')
                color = element['styles'].get('color', '#333333')
                html += f"<h1 style=\"font-size: {font_size}px; font-weight: {font_weight}; color: {color};\">{element['content']}</h1>\n"
            elif element['type'] == 'paragraph':
                font_size = element['styles'].get('font_size', 12)
                color = element['styles'].get('color', '#333333')
                line_height = element['styles'].get('line_height', 1.5)
                html += f"<p style=\"font-size: {font_size}px; color: {color}; line-height: {line_height};\">{element['content']}</p>\n"
            elif element['type'] == 'button':
                bg_color = element['styles'].get('background_color', self.accent_color)
                text_color = element['styles'].get('color', 'white')
                font_size = element['styles'].get('font_size', 12)
                font_weight = element['styles'].get('font_weight', 'bold')
                html += f"<button style=\"background-color: {bg_color}; color: {text_color}; font-size: {font_size}px; font-weight: {font_weight};\">{element['content']}</button>\n"
            elif element['type'] == 'image':
                # In a real app, use element['content'] as the image source
                html += f"<div class=\"image-placeholder\">{element['content']}</div>\n"
            elif element['type'] == 'divider':
                html += "<div class=\"divider\"></div>\n"
            elif element['type'] == 'form':
                html += """
            <div class="form-container">
                <h2>Contact Form</h2>
                <form>
                    <label for="name">Name:</label><br>
                    <input type="text" id="name" name="name"><br>
                    <label for="email">Email:</label><br>
                    <input type="email" id="email" name="email"><br>
                    <label for="message">Message:</label><br>
                    <textarea id="message" name="message" rows="5"></textarea><br>
                    <button type="submit">Submit</button>
                </form>
            </div>
            """
        
        html += """
        </div>
        </body>
        </html>"""
        
        return html


    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="Ready", bd=1, relief=tk.SUNKEN,
                                 anchor=tk.W, bg=self.bg_color, fg=self.text_color)
        self.status_bar.grid(row=1, column=0, columnspan=3, sticky="we")
        

    def update_status(self, message):
        self.status_bar.config(text=message)
        self.root.after(3000, lambda: self.status_bar.config(text="Ready"))

# This block ensures the code runs only when the script is executed directly
if __name__ == "__main__":
    root = tk.Tk()
    
    # Set theme (requires ttkthemes package - install with pip install ttkthemes)
    if ThemedStyle: # Check if ThemedStyle was successfully imported
        try:
            style = ThemedStyle(root)
            style.set_theme("arc") # Or "adapta", "plastik", etc.
        except Exception as e:
            print(f"Failed to set theme: {e}")
            pass # Continue without theme if it fails
        
    app = WebDesignApp(root)
    root.mainloop()