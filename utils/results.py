"""
Results handler: Save and load analysis results.
Provides utilities for CSV export and result persistence.
"""

import csv
from datetime import datetime
import os


def save_results_to_csv(file_path, equation, method, result, tolerance, max_iterations):
    """
    Save root finding results to CSV file.
    
    Parameters:
        file_path : str, path to save CSV
        equation : str, the equation being solved
        method : str, name of the method used
        result : dict, result dictionary from solver
        tolerance : float, convergence tolerance
        max_iterations : int, maximum iterations allowedReturns:
        bool : True if successful, False otherwise
    """
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            
            # Meta information
            writer.writerow(["Root Finding Calculator - Results"])
            writer.writerow(["Generated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
            writer.writerow([])
            
            # Configuration
            writer.writerow(["Configuration:"])
            writer.writerow(["Equation", equation])
            writer.writerow(["Method", method])
            writer.writerow(["Tolerance", tolerance])
            writer.writerow(["Max Iterations", max_iterations])
            writer.writerow([])
            
            # Results Summary
            writer.writerow(["Results Summary:"])
            writer.writerow(["Root Found", result.get("root", "N/A")])
            writer.writerow(["Iterations Performed", result.get("iterations", "N/A")])
            writer.writerow(["Converged", "Yes" if result.get("converged") else "No"])
            writer.writerow(["Final Error", result.get("errors", [None])[-1] if result.get("errors") else "N/A"])
            writer.writerow(["Message", result.get("message", "")])
            writer.writerow([])
            
            # Iteration history
            history = result.get("history", [])
            if history:
                writer.writerow(["Iteration History:"])
                keys = list(history[0].keys())
                writer.writerow(keys)
                for row_data in history:
                    writer.writerow([row_data.get(k, "") for k in keys])
        
        return True
    except Exception as e:
        print(f"Error saving results: {e}")
        return False


def load_results_from_csv(file_path):
    """
    Load previously saved results from CSV.
    
    Parameters:
        file_path : str, path to CSV file
        
    Returns:
        dict : Parsed results or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            results = {}
            
            for row in reader:
                # Parse specific rows
                if row and row[0] == "Equation":
                    results["equation"] = row[1] if len(row) > 1 else ""
                elif row and row[0] == "Method":
                    results["method"] = row[1] if len(row) > 1 else ""
                elif row and row[0] == "Root Found":
                    try:
                        results["root"] = float(row[1]) if len(row) > 1 else None
                    except ValueError:
                        results["root"] = None
            
            return results if results else None
    except Exception as e:
        print(f"Error loading results: {e}")
        return None
