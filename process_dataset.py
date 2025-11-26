"""
Process Mintlify dataset (CSV) by:
* removing entries with non-English characters in specific columns
* removing entries with empty 'query', 'response', or 'sources' fields
* removing entries with one or fewer English words in the 'query' field

Usage:
    python process_dataset.py --input_file <path_to_input_csv> --output_dir <output_directory>
"""
import argparse
import pandas as pd

def read_dataset(file_path: str) -> pd.DataFrame:
    """Reads the dataset from a CSV file and returns a DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
    """
    return pd.read_csv(file_path)

def korean_japanese_patterns() -> tuple[str, str]:
    """Returns regex patterns for Korean and Japanese characters."""
    korean_pattern = r"[\uAC00-\uD7AF]"  
    japanese_pattern = r"[\u3040-\u30FF\u4E00-\u9FFF]"
    return korean_pattern, japanese_pattern


def remove_non_english(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows with non-English characters in 'query' and 'response' columns.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    """
    korean_pattern, japanese_pattern = korean_japanese_patterns()
    JP_KR = fr"(?:{korean_pattern}|{japanese_pattern})"
    
    filtered_df = df[
        ~(
            df["query"].str.contains(JP_KR, na=False) |
            df["response"].str.contains(JP_KR, na=False)
        )
    ].copy()
    
    return filtered_df

def remove_empty_entries(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows with empty 'query' or 'response' entries.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    """
    filtered_df = df[
        df["query"].notna() & df["response"].notna() &
        (df["query"].str.strip() != "") & (df["response"].str.strip() != "[]")
    ].copy()
    
    return filtered_df


def remove_empty_sources(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows with empty 'sources' entries.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    """
    filtered_df = df[
        df["sources"].notna() & (df["sources"].str.strip() != "[]")
    ].copy()

    return filtered_df

def remove_empty_queries(df: pd.DataFrame) -> pd.DataFrame:
    """Removes entries with one or fewer English words in the 'query' column.
    
    Args:
        df (pd.DataFrame): Input DataFrame.
    """
    # (?:[-'][A-Za-z]+)* → optionally followed by hyphen/apostrophe + more letters
    word_rx = r"[A-Za-z]+(?:[-'][A-Za-z]+)*"

    # Optional: remove URLs, then find words
    url_rx = r"https?://\S+|www\.\S+"

    normalized = (
        df["query"].fillna("")
        .str.replace(url_rx, " ", regex=True)
        .str.replace(r"[^\w'\-]+", " ", regex=True)  # remove junk except hyphen/apostrophe
        .str.strip()
    )

    word_count = normalized.str.findall(word_rx).str.len()
    return df[word_count > 1].copy()

def process_dataset(file_path: str) -> pd.DataFrame:
    """Processes the dataset by reading and filtering non-English entries.
    
    Args:
        file_path (str): Path to the CSV file.
    """
    df = read_dataset(file_path)
    df_clean = remove_non_english(df)
    df_clean = remove_empty_entries(df_clean)
    df_clean = remove_empty_sources(df_clean)
    df_clean = remove_empty_queries(df_clean)
    return df_clean

def main(args):    
    # Process the Mintlify dataset
    mintlify_dataset = args.input_file
    processed_df = process_dataset(mintlify_dataset)
    print(f"Processed dataset contains {processed_df.shape[0]} entries.")

    # Save the processed dataset
    output_dir = args.output_dir
    processed_df.to_csv(f"{output_dir}processed_mintlify_dataset.csv", index=False)
    print(f"Processed dataset saved to '{output_dir}/processed_mintlify_dataset.csv'.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process Mintlify dataset to remove non-English entries.")
    parser.add_argument("--input_file", type=str, default="./OriginalDatasets/chat-export-wb-21fd5541-2025-10-15T24_00_00-2025-11-13T24_00_00.csv",
                        help="Path to the input Mintlify dataset CSV file.")
    parser.add_argument("--output_dir", type=str, default="./evaluate/ProcessedDatasets",
                        help="Directory to save the processed dataset.")
    main(parser.parse_args())