import tkinter as tk
from tkinter import ttk

class BCDCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BCD Calculator")
        self.root.geometry("550x450")
        self.root.resizable(False, False)
        
        # Create main frame
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input frame
        input_frame = ttk.LabelFrame(main_frame, text="Input Values", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        # First number input
        ttk.Label(input_frame, text="Enter BCD A (0-9):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_a = ttk.Entry(input_frame, width=10)
        self.entry_a.grid(row=0, column=1, padx=10, pady=5)
        
        # Second number input
        ttk.Label(input_frame, text="Enter BCD B (0-9):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_b = ttk.Entry(input_frame, width=10)
        self.entry_b.grid(row=1, column=1, padx=10, pady=5)
        
        # Calculate button
        calc_button = ttk.Button(
            main_frame, 
            text="Calculate BCD Addition", 
            command=self.bcd_addition_using_subtractor
        )
        calc_button.pack(pady=10)
        
        # Results frame with Text widget for list output
        results_frame = ttk.LabelFrame(main_frame, text="Results", padding="10")
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Create text widget with scrollbar for results
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, height=15, width=60)
        scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Pack the text widget and scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.results_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Configure tags for formatting
        self.results_text.tag_configure("heading", font=("Arial", 10, "bold"))
        self.results_text.tag_configure("normal", font=("Arial", 10))
        self.results_text.tag_configure("result", font=("Arial", 10, "bold"), foreground="blue")
        self.results_text.tag_configure("error", font=("Arial", 10, "bold"), foreground="red")
        
        # Status bar
        self.status_label = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Set focus to first entry
        self.entry_a.focus_set()
        
    def bcd_addition_using_subtractor(self):
        """Perform BCD addition using subtractor logic and display results as a list"""
        # Clear previous results
        self.results_text.delete(1.0, tk.END)
        
        try:
            # Get and validate inputs
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            
            if a < 0 or a > 9 or b < 0 or b > 9:
                self.display_error("Error: Both inputs must be BCD digits (0-9)")
                return
            
            # Start building the results list
            self.results_text.insert(tk.END, "1. INPUT VALUES:\n", "heading")
            self.results_text.insert(tk.END, f"   • A = {a} (Decimal) = {a:04b} (Binary)\n", "normal")
            self.results_text.insert(tk.END, f"   • B = {b} (Decimal) = {b:04b} (Binary)\n\n", "normal")
            
            # Calculate subtractor-based addition
            self.results_text.insert(tk.END, "2. SUBTRACTOR LOGIC STEPS:\n", "heading")
            
            # Two's complement calculation for subtractor logic
            b_negated = -b
            b_twos_complement = (~b_negated + 1) & 0xF  # 4-bit two's complement
            
            self.results_text.insert(tk.END, f"   • Negate B: -{b}\n", "normal")
            self.results_text.insert(tk.END, f"   • Two's Complement of -B: {b_twos_complement:04b}\n", "normal")
            
            # Calculate decimal result
            result_decimal = a + b
            self.results_text.insert(tk.END, f"   • A + B = {a} + {b} = {result_decimal} (Decimal)\n\n", "normal")
            
            # BCD correction
            self.results_text.insert(tk.END, "3. BCD CORRECTION:\n", "heading")
            
            # Apply BCD correction if needed
            bcd_corrected = result_decimal
            
            if result_decimal > 9:
                bcd_corrected = result_decimal + 6  # Add 6 for BCD correction
                self.results_text.insert(tk.END, f"   • Result {result_decimal} > 9, applying correction\n", "normal")
                self.results_text.insert(tk.END, f"   • Correction: {result_decimal} + 6 = {bcd_corrected}\n\n", "normal")
            else:
                self.results_text.insert(tk.END, f"   • Result {result_decimal} ≤ 9, no correction needed\n\n", "normal")
            
            # Ensure 4-bit representation for BCD
            result_bcd = bcd_corrected & 0xF
            
            # Final results
            self.results_text.insert(tk.END, "4. FINAL RESULTS:\n", "heading")
            self.results_text.insert(tk.END, f"   • Decimal Result: {result_decimal}\n", "result")
            self.results_text.insert(tk.END, f"   • BCD Result: {result_bcd}\n", "result")
            self.results_text.insert(tk.END, f"   • Binary Representation: {result_bcd:04b}\n", "result")
            
            # Update status
            self.status_label.config(text="Calculation completed successfully")
            
        except ValueError:
            self.display_error("Error: Please enter valid digits (0-9)")
    
    def display_error(self, message):
        """Display error message in the results text widget"""
        self.results_text.insert(tk.END, message + "\n", "error")
        self.status_label.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    app = BCDCalculator(root)
    root.mainloop()