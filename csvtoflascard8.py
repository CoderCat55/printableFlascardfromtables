import pandas as pd
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class PDFMaker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the main window
        
    def select_file(self):
        """Let user select CSV or Excel file using file dialog"""
        file_path = filedialog.askopenfilename(
            title="Select CSV or Excel File",
            filetypes=[
                ("CSV files", "*.csv"),
                ("Excel files", "*.xlsx"),
                ("Excel files", "*.xls"),
                ("All files", "*.*")
            ]
        )
        return file_path
    
    def get_pdf_filename(self):
        """Get PDF filename from user"""
        filename = simpledialog.askstring("PDF Filename", "Enter the name for the PDF file (without extension):")
        if filename:
            if not filename.endswith('.pdf'):
                filename += '.pdf'
        return filename
    
    def read_file_data(self, file_path):
        """Read Column A and Column B from CSV or Excel file"""
        try:
            if file_path.lower().endswith('.csv'):
                # Read CSV file
                df = pd.read_csv(file_path, header=None)
            elif file_path.lower().endswith(('.xlsx', '.xls')):
                # Read Excel file
                df = pd.read_excel(file_path, header=None)
            else:
                messagebox.showerror("Error", "Unsupported file format. Please use CSV or Excel files.")
                return None, None
            
            # Extract Column A (index 0) and Column B (index 1)
            column_a = []
            column_b = []
            
            # Skip first row if it's a header, otherwise include it
            start_row = 1 if df.shape[0] > 0 and isinstance(df.iloc[0, 0], str) and df.iloc[0, 0].lower() in ['column a', 'a', 'front'] else 0
            
            for i in range(start_row, len(df)):
                # Column A
                if 0 < len(df.columns):
                    val_a = df.iloc[i, 0]
                    if pd.notna(val_a):
                        column_a.append(str(val_a).strip())
                    else:
                        column_a.append("")
                
                # Column B
                if 1 < len(df.columns):
                    val_b = df.iloc[i, 1]
                    if pd.notna(val_b):
                        column_b.append(str(val_b).strip())
                    else:
                        column_b.append("")
            
            return column_a, column_b
            
        except Exception as e:
            messagebox.showerror("Error", f"Error reading file: {str(e)}")
            return None, None
    
    def create_pdf(self, column_a, column_b, output_filename):
        """Create PDF with alternating layout pattern"""
        try:
            # Page setup
            page_width, page_height = A6
            margin = 5 * mm
            
            # Calculate grid dimensions
            cols = 2
            rows = 5
            tcpp = cols * rows  # Total cells per page = 10
            cell_width = (page_width - 2 * margin) / cols
            cell_height = (page_height - 2 * margin) / rows
            
            # Create PDF
            c = canvas.Canvas(output_filename, pagesize=A6)
            
            # Calculate total pages needed
            max_words = max(len(column_a), len(column_b))
            total_pages = (max_words + tcpp - 1) // tcpp * 2  # Multiply by 2 for both A and B pages
            
            cmr = 0  # Current row marker (starts at index 0, which is row 1 in Excel)
            page_number = 1
            
            while cmr < max_words:
                if page_number > 1:
                    c.showPage()
                
                print(f"Creating Page {page_number}, cmr={cmr+1}")
                
                if page_number % 2 == 1:  # ODD page - Column A
                    # Layout: [cmr, cmr+1], [cmr+2, cmr+3], [cmr+4, cmr+5], [cmr+6, cmr+7], [cmr+8, cmr+9]
                    for row in range(rows):
                        for col in range(cols):
                            data_index = cmr + row * cols + col
                            
                            if data_index < len(column_a):
                                word = column_a[data_index]
                            else:
                                word = ""
                            
                            coord = f"{data_index + 1}A"  # +1 because Excel rows start at 1
                            self.draw_word_in_cell(c, word, row, col, cell_width, cell_height,
                                                 page_width, page_height, margin, coord)
                
                else:  # EVEN page - Column B
                    # Layout: [cmr+1, cmr], [cmr+3, cmr+2], [cmr+5, cmr+4], [cmr+7, cmr+6], [cmr+9, cmr+8]
                    for row in range(rows):
                        # Left cell: cmr + row*2 + 1 (odd index)
                        # Right cell: cmr + row*2 (even index)
                        left_index = cmr + row * 2 + 1
                        right_index = cmr + row * 2
                        
                        # Draw left cell (reversed - higher number)
                        if left_index < len(column_b):
                            word_left = column_b[left_index]
                        else:
                            word_left = ""
                        coord_left = f"{left_index + 1}B"
                        self.draw_word_in_cell(c, word_left, row, 0, cell_width, cell_height,
                                             page_width, page_height, margin, coord_left)
                        
                        # Draw right cell (reversed - lower number)
                        if right_index < len(column_b):
                            word_right = column_b[right_index]
                        else:
                            word_right = ""
                        coord_right = f"{right_index + 1}B"
                        self.draw_word_in_cell(c, word_right, row, 1, cell_width, cell_height,
                                             page_width, page_height, margin, coord_right)
                
                # Draw grid lines
                self.draw_grid_lines(c, page_width, page_height, margin, cols, rows, cell_width, cell_height)
                
                # Move to next set after completing both A and B pages
                if page_number % 2 == 0:
                    cmr += tcpp
                
                page_number += 1
            
            c.save()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Error creating PDF: {str(e)}")
            return False
    
    def draw_word_in_cell(self, c, word, row, col, cell_width, cell_height, 
                         page_width, page_height, margin, coord):
        """Draw a word in a specific cell"""
        # Calculate position
        x = margin + col * cell_width + cell_width / 2
        y = page_height - margin - row * cell_height - cell_height / 2
        
        # Configure text
        c.setFont("Helvetica", 10)
        c.setFillColorRGB(0, 0, 0)  # Black color
        
        # Split long text to fit in cell
        max_width = cell_width - 4 * mm
        wrapped_text = simpleSplit(str(word), "Helvetica", 10, max_width)
        
        # Draw text (centered)
        text_height = len(wrapped_text) * 4 * mm
        current_y = y + text_height / 2 - 2 * mm
        
        for line in wrapped_text:
            text_width = c.stringWidth(line, "Helvetica", 10)
            c.drawString(x - text_width / 2, current_y, line)
            current_y -= 4 * mm
    
    def draw_grid_lines(self, c, page_width, page_height, margin, cols, rows, cell_width, cell_height):
        """Draw grid lines for better visualization"""
        c.setStrokeColorRGB(0.8, 0.8, 0.8)  # Light gray
        c.setLineWidth(0.5)
        
        # Draw border
        c.rect(margin, margin, page_width - 2*margin, page_height - 2*margin)
        
        # Vertical lines
        for col in range(1, cols):
            x = margin + col * cell_width
            c.line(x, margin, x, page_height - margin)
        
        # Horizontal lines
        for row in range(1, rows):
            y = page_height - margin - row * cell_height
            c.line(margin, y, page_width - margin, y)
    
    def show_file_info(self, column_a, column_b, file_path):
        """Show information about the loaded file"""
        file_name = os.path.basename(file_path)
        file_type = "Excel" if file_path.lower().endswith(('.xlsx', '.xls')) else "CSV"
        max_words = max(len(column_a), len(column_b))
        total_pages = ((max_words + 9) // 10) * 2  # Both A and B pages
        
        messagebox.showinfo(
            "File Loaded", 
            f"File: {file_name}\n"
            f"Type: {file_type}\n"
            f"Column A words: {len(column_a)}\n"
            f"Column B words: {len(column_b)}\n"
            f"Pages needed: {total_pages}\n"
            f"Layout: Alternating A/B pattern"
        )
    
    def run(self):
        """Main function to run the application"""
        try:
            # Step 1: Select file using file dialog
            file_path = self.select_file()
            if not file_path:
                messagebox.showinfo("Info", "No file selected. Exiting.")
                return
            
            # Step 2: Get PDF filename
            pdf_filename = self.get_pdf_filename()
            if not pdf_filename:
                messagebox.showinfo("Info", "No PDF filename entered. Exiting.")
                return
            
            # Step 3: Read file data (Column A and Column B)
            column_a, column_b = self.read_file_data(file_path)
            if column_a is None or column_b is None:
                return
            
            if len(column_a) == 0 and len(column_b) == 0:
                messagebox.showwarning("Warning", "No data found in columns A and B.")
                return
            
            # Show file information
            self.show_file_info(column_a, column_b, file_path)
            
            # Step 4: Create PDF with correct algorithm
            success = self.create_pdf(column_a, column_b, pdf_filename)
            
            if success:
                max_words = max(len(column_a), len(column_b))
                total_pages = ((max_words + 9) // 10) * 2
                messagebox.showinfo(
                    "Success", 
                    f"PDF created successfully!\n"
                    f"File: {os.path.abspath(pdf_filename)}\n"
                    f"Column A words: {len(column_a)}\n"
                    f"Column B words: {len(column_b)}\n"
                    f"Total pages: {total_pages}"
                )
                
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")

def test_algorithm():
    """Test the algorithm with sample data"""
    print("=== Testing Algorithm ===\n")
    
    # Sample data
    column_a = [f"Word{i}" for i in range(1, 21)]
    column_b = [f"Back{i}" for i in range(1, 21)]
    
    cols = 2
    rows = 5
    tcpp = 10
    
    cmr = 0
    page_number = 1
    max_words = max(len(column_a), len(column_b))
    
    while cmr < max_words:
        print(f"Page {page_number} (cmr={cmr+1}):")
        
        if page_number % 2 == 1:  # ODD - Column A
            print("  Column A - Sequential:")
            for row in range(rows):
                left_idx = cmr + row * 2
                right_idx = cmr + row * 2 + 1
                left_word = column_a[left_idx] if left_idx < len(column_a) else "EMPTY"
                right_word = column_a[right_idx] if right_idx < len(column_a) else "EMPTY"
                print(f"  [{left_idx+1}A: {left_word}, {right_idx+1}A: {right_word}]")
        
        else:  # EVEN - Column B
            print("  Column B - Reversed pairs:")
            for row in range(rows):
                left_idx = cmr + row * 2 + 1  # Higher number on left
                right_idx = cmr + row * 2      # Lower number on right
                left_word = column_b[left_idx] if left_idx < len(column_b) else "EMPTY"
                right_word = column_b[right_idx] if right_idx < len(column_b) else "EMPTY"
                print(f"  [{left_idx+1}B: {left_word}, {right_idx+1}B: {right_word}]")
        
        if page_number % 2 == 0:
            cmr += tcpp
        
        page_number += 1
        print()

def main():
    """Main function"""
    # First show the algorithm test
    test_algorithm()
    
    # Then run the actual application
    print("\n" + "="*50)
    print("Starting PDF Maker Application...")
    print("="*50)
    
    app = PDFMaker()
    app.run()

if __name__ == "__main__":
    print("""
Required packages:
- pandas
- reportlab
- openpyxl (for Excel support)
    
Install with:
pip install pandas reportlab openpyxl
""")
    main()