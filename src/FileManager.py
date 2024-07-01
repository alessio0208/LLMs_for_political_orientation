import os

class FileManager:
    
    @staticmethod
    def select_missing_files(input_path, output_path):
        """
        Selects files from the input directory that are not present in the output directory.
        
        Parameters:
        input_path (str): Path to the directory containing input files.
        output_path (str): Path to the directory containing output files.
        
        Returns:
        set: A set of filenames that are in the input directory but missing from the output directory.
        """
        # List all files in the input directory
        input_files = os.listdir(input_path)
        
        # Create a dictionary with base filenames (excluding extensions) as keys and full filenames as values
        files_input_base = {os.path.splitext(file)[0].split('_')[0]: file for file in input_files}
        
        # Create a set of base filenames (excluding extensions) in the output directory
        files_output_base = {os.path.splitext(file)[0].split('_')[0] for file in os.listdir(output_path)}

        # Determine which files are in the input directory but missing from the output directory
        files_to_process = {files_input_base[date] for date in files_input_base if date not in files_output_base}

        return files_to_process

    @staticmethod
    def save_file(input_filename, new_filename, new_extension, output_path, df):
        """
        Saves a DataFrame to a CSV file in the specified output directory.
        
        Parameters:
        input_filename (str): Original filename used to derive the date part.
        new_filename (str): New base name for the file.
        new_extension (str): Extension for the new file.
        output_path (str): Path to the directory where the file will be saved.
        df (pd.DataFrame): DataFrame to be saved as a CSV file.
        """
        # Extract the date part from the input filename
        date_part = input_filename.split('_')[0]
        
        # Construct the new filename
        filename = f"{date_part}_{new_filename}.{new_extension}"
        
        # Save the DataFrame to a CSV file in the output directory
        df.to_csv(os.path.join(output_path, filename), index=False)
