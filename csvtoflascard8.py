# First, install required packages
!pip install -q pandas reportlab openpyxl
import pandas as pd
from reportlab.lib.pagesizes import A6
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import os
from google.colab import files

class ColabPDFMaker:
    def __init__(self):
        self.fontsize = 10  # Default font size

    def upload_file(self):
        """Upload CSV or Excel file in Google Colab"""
        print("Please upload your CSV or Excel file:")
        uploaded = files.upload()

        if not uploaded:
            print("No file uploaded. Exiting.")
            return None

        # Get the uploaded filename
        filename = list(uploaded.keys())[0]

        # Save the uploaded file
        with open(filename, 'wb') as f:
            f.write(uploaded[filename])

        print(f"File '{filename}' uploaded successfully!")
        return filename

    def get_fontsize(self):
        """Get font size from user"""
        try:
            fontsize = float(input("Enter font size (default is 10): ") or "10")
            return fontsize
        except ValueError:
            print("Invalid font size. Using default size 10.")
            return 10

    def get_pdf_filename(self):
        """Get PDF filename from user"""
        filename = input("Enter the name for the PDF file (without extension): ")
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
                print("Error: Unsupported file format. Please use CSV or Excel files.")
                return None, None

            # Extract Column A (index 0) and Column B (index 1)
            column_a = []
            column_b = []

            # Skip first row if it's a header
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
            print(f"Error reading file: {str(e)}")
            return None, None

    def create_pdf(self, column_a, column_b, output_filename, fontsize):
        """Create PDF with alternating layout pattern"""
        try:
            # Page setup
            page_width, page_height = A6
            margin = 8 * mm

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
                                                 page_width, page_height, margin, coord, fontsize)

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
                                             page_width, page_height, margin, coord_left, fontsize)

                        # Draw right cell (reversed - lower number)
                        if right_index < len(column_b):
                            word_right = column_b[right_index]
                        else:
                            word_right = ""
                        coord_right = f"{right_index + 1}B"
                        self.draw_word_in_cell(c, word_right, row, 1, cell_width, cell_height,
                                             page_width, page_height, margin, coord_right, fontsize)

                # Draw grid lines
                self.draw_grid_lines(c, page_width, page_height, margin, cols, rows, cell_width, cell_height)

                # Move to next set after completing both A and B pages
                if page_number % 2 == 0:
                    cmr += tcpp

                page_number += 1

            c.save()
            return True

        except Exception as e:
            print(f"Error creating PDF: {str(e)}")
            return False

    def draw_word_in_cell(self, c, word, row, col, cell_width, cell_height,
                         page_width, page_height, margin, coord, fontsize):
        """Draw a word in a specific cell"""
        # Calculate position
        x = margin + col * cell_width + cell_width / 2
        y = page_height - margin - row * cell_height - cell_height / 2

        # Configure text
        c.setFont("Helvetica", fontsize)
        c.setFillColorRGB(0, 0, 0)  # Black color

        # Split long text to fit in cell
        max_width = cell_width - 4 * mm
        wrapped_text = simpleSplit(str(word), "Helvetica", fontsize, max_width)

        # Draw text (centered)
        text_height = len(wrapped_text) * (fontsize / 2.5) * mm
        current_y = y + text_height / 2 - (fontsize / 5) * mm

        for line in wrapped_text:
            text_width = c.stringWidth(line, "Helvetica", fontsize)
            c.drawString(x - text_width / 2, current_y, line)
            current_y -= (fontsize / 2.5) * mm

    def draw_grid_lines(self, c, page_width, page_height, margin, cols, rows, cell_width, cell_height):
        """Draw grid lines for better visualization"""
        c.setStrokeColorRGB(0, 0, 0)  # black
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

        print("\n" + "="*50)
        print("FILE INFORMATION")
        print("="*50)
        print(f"File: {file_name}")
        print(f"Type: {file_type}")
        print(f"Column A words: {len(column_a)}")
        print(f"Column B words: {len(column_b)}")
        print(f"Pages needed: {total_pages}")
        print(f"Layout: Alternating A/B pattern")
        print("="*50 + "\n")

    def run(self):
        """Main function to run the application"""
        try:
            # Step 1: Get font size from user
            self.fontsize = self.get_fontsize()

            # Step 2: Upload file in Google Colab
            file_path = self.upload_file()
            if not file_path:
                return

            # Step 3: Get PDF filename
            pdf_filename = self.get_pdf_filename()
            if not pdf_filename:
                print("No PDF filename entered. Exiting.")
                return

            # Step 4: Read file data (Column A and Column B)
            column_a, column_b = self.read_file_data(file_path)
            if column_a is None or column_b is None:
                return

            if len(column_a) == 0 and len(column_b) == 0:
                print("Warning: No data found in columns A and B.")
                return

            # Show file information
            self.show_file_info(column_a, column_b, file_path)

            # Step 5: Create PDF with correct algorithm
            print("Creating PDF...")
            success = self.create_pdf(column_a, column_b, pdf_filename, self.fontsize)

            if success:
                max_words = max(len(column_a), len(column_b))
                total_pages = ((max_words + 9) // 10) * 2

                print("\n" + "="*50)
                print("SUCCESS!")
                print("="*50)
                print(f"PDF created successfully!")
                print(f"File: {os.path.abspath(pdf_filename)}")
                print(f"Font size used: {self.fontsize}")
                print(f"Column A words: {len(column_a)}")
                print(f"Column B words: {len(column_b)}")
                print(f"Total pages: {total_pages}")
                print("="*50)

                # Offer to download the PDF
                print("\nWould you like to download the PDF file?")
                files.download(pdf_filename)

        except Exception as e:
            print(f"An unexpected error occurred: {str(e)}")

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
    """Main function for Google Colab"""
    print("="*60)
    print("PDF Booklet maker in google")
    print("="*60)
    print("\nThis tool creates PDF flashcards from CSV/Excel files.")
    print("Expected file format:")
    print("- Column A: Front of flashcards (odd pages)")
    print("- Column B: Back of flashcards (even pages)")
    print("="*60 + "\n")
    print("\n" + "="*60)
    print("STARTING PDF CREATION")
    print("="*60)

    # Run the application
    app = ColabPDFMaker()
    app.run()

if __name__ == "__main__":
    # First, check and install required packages
    print("Checking and installing required packages...")
    try:
        import pandas
        import reportlab
    except ImportError:
        print("Installing required packages...")
        !pip install pandas reportlab openpyxl

    print("\nRequired packages installed/verified:")
    print("- pandas")
    print("- reportlab")
    print("- openpyxl (for Excel support)")
    print("\n" + "="*60)

    main()
