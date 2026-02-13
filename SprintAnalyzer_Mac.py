#!/usr/bin/env python3
"""
Sprint Analysis Automation - Mac App
Double-click to run, drag & drop your Excel file, get results!
"""

import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import openpyxl
from datetime import datetime
import threading

# Add the automation modules to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

try:
    from automation.data_processor import SprintDataProcessor
    from automation.calculator import SprintCalculator
    from automation.excel_updater import ExcelUpdater
    from automation.notion_exporter import NotionExporter
except ImportError:
    # If running as standalone, use bundled modules
    pass


class SprintAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sprint Analysis Automation")
        self.root.geometry("800x600")
        self.root.configure(bg='#F8FAFC')
        
        # Variables
        self.file_path = None
        self.processing = False
        
        # Configure style
        self.setup_styles()
        
        # Create UI
        self.create_ui()
        
    def setup_styles(self):
        """Setup custom styles"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', 
                       font=('Helvetica Neue', 28, 'bold'),
                       foreground='#1E293B',
                       background='#F8FAFC')
        
        style.configure('Subtitle.TLabel',
                       font=('Helvetica Neue', 14),
                       foreground='#64748B',
                       background='#F8FAFC')
        
        style.configure('Card.TFrame',
                       background='white',
                       relief='flat')
        
        style.configure('Info.TLabel',
                       font=('SF Mono', 11),
                       foreground='#475569',
                       background='white')
        
        style.configure('Status.TLabel',
                       font=('Helvetica Neue', 12),
                       foreground='#1E293B',
                       background='white')
        
        style.configure('Success.TLabel',
                       font=('Helvetica Neue', 12, 'bold'),
                       foreground='#10B981',
                       background='white')
        
    def create_ui(self):
        """Create the user interface"""
        # Main container
        main_frame = tk.Frame(self.root, bg='#F8FAFC', padx=40, pady=30)
        main_frame.pack(fill='both', expand=True)
        
        # Header
        header_frame = tk.Frame(main_frame, bg='#F8FAFC')
        header_frame.pack(fill='x', pady=(0, 30))
        
        title = ttk.Label(header_frame, 
                         text="📊 Sprint Analysis",
                         style='Title.TLabel')
        title.pack()
        
        subtitle = ttk.Label(header_frame,
                            text="Upload your Excel file and get instant analysis",
                            style='Subtitle.TLabel')
        subtitle.pack(pady=(5, 0))
        
        # Card container
        card = tk.Frame(main_frame, bg='white', relief='flat', bd=0)
        card.pack(fill='both', expand=True)
        
        # Add shadow effect (simulated with nested frames)
        shadow = tk.Frame(main_frame, bg='#E2E8F0', relief='flat')
        shadow.place(in_=card, relx=0.005, rely=0.005, relwidth=1, relheight=1)
        card.lift()
        
        # Card content
        card_content = tk.Frame(card, bg='white', padx=30, pady=30)
        card_content.pack(fill='both', expand=True)
        
        # Upload section
        self.upload_frame = tk.Frame(card_content, bg='white')
        self.upload_frame.pack(fill='both', expand=True)
        
        upload_box = tk.Frame(self.upload_frame, 
                             bg='#F8FAFC',
                             relief='solid',
                             bd=2,
                             highlightbackground='#E2E8F0',
                             highlightthickness=2)
        upload_box.pack(fill='both', expand=True, pady=20)
        
        upload_icon = tk.Label(upload_box,
                              text="📁",
                              font=('Helvetica Neue', 60),
                              bg='#F8FAFC',
                              fg='#94A3B8')
        upload_icon.pack(pady=(40, 20))
        
        upload_text = tk.Label(upload_box,
                              text="Click to select your Sprint Excel file",
                              font=('Helvetica Neue', 16),
                              bg='#F8FAFC',
                              fg='#475569')
        upload_text.pack()
        
        upload_hint = tk.Label(upload_box,
                              text="or drag and drop here",
                              font=('Helvetica Neue', 12),
                              bg='#F8FAFC',
                              fg='#94A3B8')
        upload_hint.pack(pady=(5, 40))
        
        # Make it clickable
        upload_box.bind('<Button-1>', lambda e: self.select_file())
        upload_icon.bind('<Button-1>', lambda e: self.select_file())
        upload_text.bind('<Button-1>', lambda e: self.select_file())
        upload_hint.bind('<Button-1>', lambda e: self.select_file())
        
        # File info section (hidden initially)
        self.info_frame = tk.Frame(card_content, bg='white')
        
        info_label = ttk.Label(self.info_frame,
                              text="📄 File Information",
                              font=('Helvetica Neue', 16, 'bold'),
                              foreground='#1E293B',
                              background='white')
        info_label.pack(anchor='w', pady=(0, 15))
        
        self.file_name_label = ttk.Label(self.info_frame, style='Info.TLabel')
        self.file_size_label = ttk.Label(self.info_frame, style='Info.TLabel')
        self.sprint_name_label = ttk.Label(self.info_frame, style='Info.TLabel')
        
        self.file_name_label.pack(anchor='w', pady=5)
        self.file_size_label.pack(anchor='w', pady=5)
        self.sprint_name_label.pack(anchor='w', pady=5)
        
        # Process button
        button_frame = tk.Frame(self.info_frame, bg='white')
        button_frame.pack(pady=20)
        
        self.process_btn = tk.Button(button_frame,
                                     text="⚡ Process Sprint Data",
                                     font=('Helvetica Neue', 14, 'bold'),
                                     bg='#3B82F6',
                                     fg='white',
                                     relief='flat',
                                     padx=30,
                                     pady=12,
                                     cursor='hand2',
                                     command=self.process_file)
        self.process_btn.pack()
        
        # Progress section (hidden initially)
        self.progress_frame = tk.Frame(card_content, bg='white')
        
        progress_label = ttk.Label(self.progress_frame,
                                  text="🔄 Processing...",
                                  font=('Helvetica Neue', 16, 'bold'),
                                  foreground='#1E293B',
                                  background='white')
        progress_label.pack(anchor='w', pady=(0, 15))
        
        self.progress_bar = ttk.Progressbar(self.progress_frame,
                                           length=400,
                                           mode='determinate')
        self.progress_bar.pack(fill='x', pady=10)
        
        self.status_text = tk.Text(self.progress_frame,
                                  height=8,
                                  font=('SF Mono', 10),
                                  bg='#F8FAFC',
                                  fg='#475569',
                                  relief='flat',
                                  padx=15,
                                  pady=15)
        self.status_text.pack(fill='both', expand=True, pady=10)
        
        # Results section (hidden initially)
        self.results_frame = tk.Frame(card_content, bg='white')
        
        success_label = ttk.Label(self.results_frame,
                                 text="✅ Analysis Complete!",
                                 style='Success.TLabel')
        success_label.pack(pady=(0, 20))
        
        results_text = tk.Label(self.results_frame,
                               text="Your sprint has been analyzed.\nAll KPIs and metrics have been calculated.",
                               font=('Helvetica Neue', 12),
                               bg='white',
                               fg='#64748B',
                               justify='center')
        results_text.pack(pady=10)
        
        # Metrics display
        self.metrics_frame = tk.Frame(self.results_frame, bg='white')
        self.metrics_frame.pack(pady=20)
        
        # Download button
        download_btn = tk.Button(self.results_frame,
                                text="⬇️ Open Analyzed File",
                                font=('Helvetica Neue', 14, 'bold'),
                                bg='#10B981',
                                fg='white',
                                relief='flat',
                                padx=30,
                                pady=12,
                                cursor='hand2',
                                command=self.open_result_file)
        download_btn.pack(pady=10)
        
        new_file_btn = tk.Button(self.results_frame,
                                text="Process Another File",
                                font=('Helvetica Neue', 12),
                                bg='#F8FAFC',
                                fg='#3B82F6',
                                relief='flat',
                                padx=20,
                                pady=8,
                                cursor='hand2',
                                command=self.reset)
        new_file_btn.pack()
        
        # Footer
        footer = tk.Label(main_frame,
                         text="All processing happens locally on your Mac. No data is sent anywhere.",
                         font=('Helvetica Neue', 10),
                         bg='#F8FAFC',
                         fg='#94A3B8')
        footer.pack(side='bottom', pady=(20, 0))
        
    def select_file(self):
        """Open file dialog to select Excel file"""
        file_path = filedialog.askopenfilename(
            title="Select Sprint Excel File",
            filetypes=[("Excel files", "*.xlsx *.xlsm"), ("All files", "*.*")]
        )
        
        if file_path:
            self.file_path = file_path
            self.show_file_info()
    
    def show_file_info(self):
        """Display file information"""
        if not self.file_path:
            return
        
        # Hide upload frame
        self.upload_frame.pack_forget()
        
        # Show info frame
        self.info_frame.pack(fill='both', expand=True)
        
        # Get file info
        file_name = os.path.basename(self.file_path)
        file_size = os.path.getsize(self.file_path)
        
        self.file_name_label.config(text=f"File: {file_name}")
        self.file_size_label.config(text=f"Size: {self.format_bytes(file_size)}")
        
        # Try to read sprint name
        try:
            wb = openpyxl.load_workbook(self.file_path, data_only=True)
            data_sheet = wb['Data']
            sprint_name = data_sheet['C3'].value
            self.sprint_name_label.config(text=f"Sprint: {sprint_name}")
        except Exception as e:
            self.sprint_name_label.config(text="Sprint: Unable to read")
    
    def format_bytes(self, bytes_size):
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_size < 1024.0:
                return f"{bytes_size:.1f} {unit}"
            bytes_size /= 1024.0
    
    def process_file(self):
        """Process the Excel file"""
        if self.processing:
            return
        
        self.processing = True
        
        # Hide info frame, show progress
        self.info_frame.pack_forget()
        self.progress_frame.pack(fill='both', expand=True)
        
        # Clear status
        self.status_text.delete(1.0, tk.END)
        self.progress_bar['value'] = 0
        
        # Run processing in thread to keep UI responsive
        thread = threading.Thread(target=self.run_automation)
        thread.daemon = True
        thread.start()
    
    def run_automation(self):
        """Run the automation process"""
        try:
            steps = [
                "Loading workbook...",
                "Extracting sprint metadata...",
                "Processing Azure DevOps data...",
                "Validating data quality...",
                "Loading capacity data...",
                "Calculating staff metrics...",
                "Calculating team metrics...",
                "Computing CMMI measures...",
                "Updating analysis sheets...",
                "Generating Excel formulas...",
                "Saving workbook..."
            ]
            
            total_steps = len(steps)
            
            for i, step in enumerate(steps):
                self.update_status(f"[{i+1}/{total_steps}] {step}")
                self.update_progress((i + 1) / total_steps * 100)
                
                # Actual processing happens here
                if i == 0:
                    # Load workbook
                    self.wb = openpyxl.load_workbook(self.file_path, data_only=False)
                elif i == 1:
                    # Extract metadata
                    self.processor = SprintDataProcessor(self.file_path)
                    self.sprint_metadata = self.processor.extract_sprint_metadata(self.wb['Data'])
                elif i == 2:
                    # Process data
                    df_azure = pd.read_excel(self.file_path, sheet_name='Data', header=20)
                    self.azure_data = self.processor.process_azure_data(df_azure)
                elif i == 3:
                    # Validate
                    validation = self.processor.validate_data(self.azure_data)
                    if validation['status'] == 'error':
                        raise Exception("Data validation failed")
                elif i == 4:
                    # Capacity
                    self.capacity_data = self.processor.get_capacity_data(self.wb['Capacity'])
                elif i == 5:
                    # Staff metrics
                    self.calculator = SprintCalculator()
                    staff_agg = self.processor.aggregate_by_staff(self.azure_data)
                    self.staff_metrics = self.calculator.calculate_staff_metrics(
                        staff_agg, self.capacity_data, self.azure_data
                    )
                elif i == 6:
                    # Team metrics
                    team_agg = self.processor.aggregate_by_team(self.azure_data)
                    self.team_metrics = self.calculator.calculate_team_metrics(
                        team_agg, self.capacity_data, self.azure_data
                    )
                elif i == 7:
                    # CMMI
                    self.cmmi_measures = self.calculator.calculate_cmmi_measures(
                        self.sprint_metadata, self.azure_data
                    )
                elif i == 8:
                    # Update sheets
                    self.updater = ExcelUpdater(self.file_path)
                    sprint_name = self.sprint_metadata['sprint_name']
                    self.updater.update_analysis_sheet(sprint_name, self.staff_metrics, self.team_metrics)
                    self.updater.update_kpi_indicators_sheet(self.staff_metrics, self.team_metrics, sprint_name)
                    self.updater.append_to_historical_staff(self.staff_metrics, sprint_name)
                    self.updater.append_to_historical_team(self.team_metrics, sprint_name)
                    self.updater.update_cmmi_template(self.cmmi_measures, sprint_name)
                elif i == 10:
                    # Save
                    self.updater.save()
            
            # Show results
            self.root.after(500, self.show_results)
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(
                "Processing Error",
                f"An error occurred:\n\n{str(e)}\n\nPlease check your Excel file and try again."
            ))
            self.root.after(0, self.reset)
        finally:
            self.processing = False
    
    def update_status(self, message):
        """Update status text"""
        def _update():
            self.status_text.insert(tk.END, message + "\n")
            self.status_text.see(tk.END)
        
        self.root.after(0, _update)
    
    def update_progress(self, value):
        """Update progress bar"""
        def _update():
            self.progress_bar['value'] = value
        
        self.root.after(0, _update)
    
    def show_results(self):
        """Show results screen"""
        # Hide progress
        self.progress_frame.pack_forget()
        
        # Clear metrics frame
        for widget in self.metrics_frame.winfo_children():
            widget.destroy()
        
        # Create metrics grid
        metrics = [
            ("Staff Analyzed", len(self.staff_metrics)),
            ("Teams Processed", len(self.team_metrics)),
            ("Avg Team KPI", f"{self.team_metrics['kpi'].mean():.2f}"),
            ("CMMI Completion", f"{self.cmmi_measures['completion_rate']*100:.0f}%")
        ]
        
        row_frame = tk.Frame(self.metrics_frame, bg='white')
        row_frame.pack()
        
        for label, value in metrics:
            metric_card = tk.Frame(row_frame, bg='#F8FAFC', padx=20, pady=15)
            metric_card.pack(side='left', padx=10)
            
            tk.Label(metric_card,
                    text=label,
                    font=('Helvetica Neue', 10),
                    bg='#F8FAFC',
                    fg='#64748B').pack()
            
            tk.Label(metric_card,
                    text=str(value),
                    font=('SF Mono', 24, 'bold'),
                    bg='#F8FAFC',
                    fg='#1E293B').pack()
        
        # Show results frame
        self.results_frame.pack(fill='both', expand=True)
    
    def open_result_file(self):
        """Open the processed file"""
        os.system(f'open "{self.file_path}"')
    
    def reset(self):
        """Reset to initial state"""
        self.file_path = None
        self.processing = False
        
        # Hide all frames
        self.info_frame.pack_forget()
        self.progress_frame.pack_forget()
        self.results_frame.pack_forget()
        
        # Show upload frame
        self.upload_frame.pack(fill='both', expand=True)


def main():
    root = tk.Tk()
    app = SprintAnalyzerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
