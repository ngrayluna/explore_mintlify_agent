import os
import argparse
import datetime
import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def read_csv(file_path: str) -> pd.DataFrame:
    """Reads a CSV file and returns a DataFrame.
    
    Args:
        file_path (str): Path to the CSV file.
    """
    return pd.read_csv(file_path)


def calculate_score_distribution(judge_output_df: pd.DataFrame) -> list[float]:
    """Calculates the distribution of scores in the judge output DataFrame.
    
    Args:
        judge_output_df (pd.DataFrame): DataFrame containing judge outputs with a 'score' column.
    """
    print("Calculating score distribution...")
    score_percent_3 =  (judge_output_df[judge_output_df['score'] == 3].shape[0] / judge_output_df.shape[0]) * 100
    score_percent_2 =  (judge_output_df[judge_output_df['score'] == 2].shape[0] / judge_output_df.shape[0]) * 100
    score_percent_1 =  (judge_output_df[judge_output_df['score'] == 1].shape[0] / judge_output_df.shape[0]) * 100

    return [score_percent_3, score_percent_2, score_percent_1]

def pie_chart(score_distribution: list[float], timerange: tuple[datetime.datetime, datetime.datetime]) -> None:
    """Generates a pie chart for the score distribution.
    
    Args:
        score_distribution (list[float]): List containing percentage of scores [score 3, score 2, score 1].
    """
    print("Generating score distribution pie chart...")
    labels = ['Score 3', 'Score 2', 'Score 1']
    score_definition = ['Score 3: Excellent', 'Score 2: Good', 'Score 1: Poor'] 
    
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    colors = sns.color_palette('rainbow')[0:3]
    wedges, texts, autotexts  = ax.pie(score_distribution, labels=labels, colors=colors, autopct='%1.1f%%')
    ax.legend(wedges, score_definition,
          title="Score definitions",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
    ax.set_title(f'Score Distribution from {timerange[0].strftime("%Y-%m-%d")} to {timerange[1].strftime("%Y-%m-%d")}', loc='center')
    plt.tight_layout()
    plt.savefig(f'{check_plot_directory()}/score_distribution_pie_chart.png', dpi=300)
    plt.close()


def check_plot_directory() -> str:
    """Checks if the plot directory exists, creates it if not."""
    date_str = datetime.date.today().isoformat()
    plot_dir = f'Plots/{date_str}'
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    return plot_dir

def calculate_interquartile_range(data: pd.Series) -> float:
    """Calculates the interquartile range (IQR) of a pandas Series.
    
    Args:
        data (pd.Series): Input data series.
    """
    Q3 = data.quantile(0.75)
    Q1 = data.quantile(0.25)

    lower_bound, upper_bound = IQR_bounds(Q3, Q1)
    return lower_bound, upper_bound

def IQR_bounds(q3, q1) -> tuple[float, float]:
    """Calculates the lower and upper bounds for outliers using the IQR method.
    
    Args:
        data (pd.Series): Input data series.
    """
    IQR = q3 - q1
    lower_bound = q1 - 1.5 * IQR
    upper_bound = q3 + 1.5 * IQR
    return lower_bound, upper_bound

def get_urls(series: pd.Series):
    """Get URLs from `source` column."""
    all_urls = []
    for entry in series["sources"].dropna():
        try:
            items = json.loads(entry)
            for item in items:
                url = item.get("url")
                if url:
                    all_urls.append(url)
        except json.JSONDecodeError:
            # Skip malformed JSON
            continue
    return all_urls

def url_reference_plot(urls: list[str], num: int, timerange: tuple[datetime.datetime, datetime.datetime]) -> None:
    """Generates a plot for URL references.
    
    Args:
        urls (list[str]): List of URLs.
    """
    print("Generating URL reference plot...")
    url_counts = pd.Series(urls).value_counts().head(num)
    url_counts.sort_values(ascending=False).reset_index(drop=True)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=url_counts.values, y=url_counts.index, hue=url_counts.index, legend=False, palette='viridis')
    plt.xlabel('Number of References')
    plt.ylabel('URLs')
    plt.title(f'Top {num} Referenced URLs from {timerange[0].strftime("%Y-%m-%d")} to {timerange[1].strftime("%Y-%m-%d")}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{check_plot_directory()}/top_referenced_urls.png', dpi=300)
    plt.close()


def main(args):

    # Read in processed dataset
    processed_mintlify_df = read_csv(args.processed_dataset)

    # Read in judge output
    judge_output_df = read_csv(args.judge_output)

    # Check the plot directory exists
    check_plot_directory()

    # Calculate and plot score distribution
    score_distribution = calculate_score_distribution(judge_output_df)

    # Combine processed dataset with judge output
    combined_df = pd.concat([processed_mintlify_df.reset_index(drop=True), judge_output_df.reset_index(drop=True)], axis=1)

    # Count the length of each query
    combined_df['query_length'] = combined_df['query'].apply(lambda x: len(str(x).split()))

    # Ensure timestamp column is in datetime format
    combined_df["timestamp"] = pd.to_datetime(combined_df["timestamp"])

    # Find the time range of the dataset
    min_timestamp = combined_df["timestamp"].min()
    max_timestamp = combined_df["timestamp"].max()
    print(f"Dataset time range: {min_timestamp} to {max_timestamp}")

    # Generate pie chart for score distribution
    pie_chart(score_distribution, timerange=(min_timestamp, max_timestamp))

    # Calculate IQR bounds
    lower_bound, upper_bound = calculate_interquartile_range(combined_df['query_length'])

    # Calculate IQR bounds for query lengths
    filtered_df = combined_df[(combined_df['query_length'] >= lower_bound) & (combined_df['query_length'] <= upper_bound)]

    # Get URLs from the filtered DataFrame
    urls = get_urls(filtered_df)

    # Generate URL reference plot
    top_n = 20
    url_reference_plot(urls, top_n, timerange=(min_timestamp, max_timestamp))

    print(f"Analysis complete. Plots saved in the {check_plot_directory()} directory.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze judge output for processed Mintlify dataset.")
    parser.add_argument("--processed_dataset", type=str, help="Path to the processed Mintlify dataset CSV file.")
    parser.add_argument("--judge_output", type=str, help="Path to the judge output CSV file.")
    main(parser.parse_args())