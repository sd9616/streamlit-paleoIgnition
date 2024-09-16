import base64
from io import BytesIO
import zipfile
import matplotlib.pyplot as plt 
import streamlit as st
import numpy as np
import os
import pandas as pd
import plotly.express as px

st.markdown("""
            ## Lightning Time Series Plotter
            
            * Generate a time series for any site/location!
            * After hitting generate scroll to the bottom of the page to download a png of plot + CSV files containing the time series data.
            """)

# Select a Dataset
chosen_dataset = st.selectbox(
    "Pick a Dataset to plot or choose all!",
    ("TraCE", "FAMOUS", "LOVECLIM", "All"))


# Enter lat and Lon
lat_point = st.number_input('Latitude Point (between -90 and 90)', -90.0, 90.0, step=1e-2, format="%.5f")
lon_point = st.number_input('Longitude Point (between 0 and 360)', 0.0, 360.0, step=1e-2, format="%.5f")


# Hit generate
col1, col2, col3, col4 = st.columns([0.20, 0.65, 0.1, 0.15])

generate = col1.button("Generate", type="primary")
    
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(project_path)

file_path = os.path.join(project_path, 'data')

TRACE = "TRACE"
FAMOUS = "FAMOUS"
LOVECLIM = "LOVECLIM"

def load_a_dataset(dataset): 
    
    if dataset == TRACE: 
        dataset_short_form = "tr"
        
    elif dataset == FAMOUS: 
        dataset_short_form = "fa"
        
    elif dataset == LOVECLIM: 
        dataset_short_form = "lc"
        
    else: 
        print(f"ERROR: {dataset} is not a valid option")
        return
    
    dataset_files = [
        np.load(os.path.join(file_path, f'{dataset_short_form}_rolling_avg_trimmed.npy')),
        np.load(os.path.join(file_path, f'{dataset_short_form}_lat.npy')),
        np.load(os.path.join(file_path, f'{dataset_short_form}_lon.npy')) 
    ]
    
    return dataset_files
    
def load_datasets(dataset):
    dataset_files_list = {}
    if dataset == "All": 
        loveclim_files = load_a_dataset(LOVECLIM)
        trace_files = load_a_dataset(TRACE)
        famous_files = load_a_dataset(FAMOUS)
        
        dataset_files_list[FAMOUS] = famous_files
        dataset_files_list[TRACE] = trace_files
        dataset_files_list[LOVECLIM] = loveclim_files        
        
    if dataset == LOVECLIM: 
        loveclim_files = load_a_dataset(LOVECLIM)
        dataset_files_list[LOVECLIM] = loveclim_files   

    if dataset == TRACE:   
        trace_files = load_a_dataset(TRACE)
        dataset_files_list[TRACE] = trace_files

    if dataset == FAMOUS: 
        famous_files = load_a_dataset(FAMOUS)
        dataset_files_list[FAMOUS] = famous_files

    time = np.load(os.path.join(file_path, 'time_rolling_21_0.4.npy'))

    return dataset_files_list, time
       
# Returned file buffer to convert to a CSV file
def np_to_csv(col1_name, col1_data, col2_name, col2_data): 
    data = {f'{col1_name}': col1_data, f'{col2_name}': col2_data}
    df = pd.DataFrame(data)
    csv_buffer = BytesIO()
    df.to_csv(csv_buffer, index=False)
    csv_buffer.seek(0)  # Move to the start of the BytesIO object
    return csv_buffer

def create_df(selected_frame, time, key): 
    
    df = pd.DataFrame({'lightning': selected_frame, 'time': time, 'dataset': key})
    
    return df
    
def get_selected_frame(dataset_files, lat_point, lon_point): 
    var, lat, lon = dataset_files
        
    lat_idx = np.argmin(np.abs(lat - lat_point))
    lon_idx = np.argmin(np.abs(lon - lon_point))

    return var[:, lat_idx, lon_idx]
    
def plot_scrollable_series(datasets, time): 
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    data_set = []
    data_frames = []

    csvs = {}

    # Generated the frame for each data set
    for key, dataset_files in datasets.items():

        selected_frame = get_selected_frame(dataset_files, lat_point, lon_point)
        df = create_df(selected_frame, time, key)

        data_frames.append(df)

        print(f"generating {key} CSV")
        csv = np_to_csv("Time (kaBP)", time, "Lightning (mm/day)", selected_frame)
        csvs[f"{key}_{lat_point}_{lon_point}.csv"] = csv
        
    # Combine all data frames into one
    combined_data = pd.concat(data_frames, ignore_index=True)
    
    fig = px.line(combined_data, x='time', y='lightning', color='dataset',
                title=f'Time series of lightning at {lat_point}, {lon_point}',
                labels={'time': 'Time (kaBP)', 'lightning': 'Lightning (mm/day)'},
                color_discrete_map={'TRACE': 'blue', 'FAMOUS': 'green', 'LOVECLIM': 'orange'})

    fig.update_traces(mode='lines', showlegend=True)

    fig.update_layout(xaxis_title='Time (kaBP)', yaxis_title='Lightning (mm/day)')
    
    st.plotly_chart(fig, use_container_width=True)

    return csvs

def plot_a_scrollable_series(dataset_name, datasets, time): 
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    data_set = []
    data_frames = []

    csvs = {}
    
    dataset_files = datasets[dataset_name]
    
    # Generated the frame for each data set
    selected_frame = get_selected_frame(dataset_files, lat_point, lon_point)
    df = create_df(selected_frame, time, dataset_name)

    data_frames.append(df)

    csv = np_to_csv("Time (kaBP)", time, "Lightning (mm/day)", selected_frame)
    csvs[f"{dataset_name}_{lat_point}_{lon_point}.csv"] = csv
    
    # Combine all data frames into one
    combined_data = pd.concat(data_frames, ignore_index=True)
    
    fig = px.line(combined_data, x='time', y='lightning', color='dataset',
                title=f'{dataset_name}: Time series of lightning at {lat_point}, {lon_point}',
                labels={'time': 'Time (kaBP)', 'lightning': 'Lightning (mm/day)'},
                color_discrete_map={'TRACE': 'blue', 'FAMOUS': 'green', 'LOVECLIM': 'orange'})

    fig.update_traces(mode='lines', showlegend=True)

    fig.update_layout(xaxis_title='Time (kaBP)', yaxis_title='Lightning (mm/day)')
    
    st.plotly_chart(fig, use_container_width=True)

    return csvs

def plot_graph_time_series(datasets, time):
    
    plt.figure(figsize=(10, 6))

    csvs = {}
    
    for key, dataset_files in datasets.items():

        selected_frame = get_selected_frame(dataset_files, lat_point, lon_point)
        
        plt.plot(time, selected_frame, label=f'{key}')
        
        csv = np_to_csv("Time (kaBP)", time, "Lightning (mm/day)", selected_frame)
        csvs[f"{key}_{lat_point}_{lon_point}.csv"] = csv

    plt.xlabel('Time')
    plt.ylabel('Lightning')
    plt.title(f'All Datasets: Time series of Lightning at {lat_point}, {lon_point}')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    # Save plot to a BytesIO buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Display the plot using Streamlit
    st.pyplot(plt)
    

    # Close the plot to prevent memory leaks
    plt.close()
    
    return csvs, img_buffer

def plot_a_graph_time_series(dataset_name, datasets, time):
    """Given dataset_name, plots a static plot for a given dataset. 
    
    Args: 
        dataset_name: the dataset chosen by the user, in all caps
        
    Returns: 
        csvs: buffer containing contents of the time series data
        img_buffer: buffer containing contents of the image
    """
    
    # Color map for time series 
    color_map = {
        "TRACE": "blue",
        "LOVECLIM": "orange",
        "FAMOUS": "green"
    }
    
    plt.figure(figsize=(10, 6))

    csvs = {}
    
    dataset_files = datasets[dataset_name]

    selected_frame = get_selected_frame(dataset_files, lat_point, lon_point)
    
    plt.plot(time, selected_frame, label=f'{dataset_name}', color=color_map.get(dataset_name, 'black'))
    
    csv = np_to_csv("Time (kaBP)", time, "Lightning (mm/day)", selected_frame)
    csvs[f"{dataset_name}_{lat_point}_{lon_point}.csv"] = csv

    plt.xlabel('Time')
    plt.ylabel('Lightning')
    plt.title(f'{dataset_name}: Time series of Lightning at {lat_point}, {lon_point}')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    # Save plot to a BytesIO buffer
    img_buffer = BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    
    # Display the plot using Streamlit
    st.pyplot(plt)

    # Close the plot to prevent memory leaks
    plt.close()
    
    return csvs, img_buffer
        
def create_download_link(file_buffer, filename, link_description, file_type='application/zip'):
    """Given a buffer, generates a download link for its contents. 
    
    Args: 
        file_buffer: a buffer object containing the contents for the download link
        filename: name of the file when downloaded
        link_description: hyperlinks title when rendered on site 
        file_type: type of file, 'application/zip' by default
        
    Returns: 
        hyper-link to contents in file_buffer
    """
    file_buffer.seek(0)  # Ensure the buffer is at the beginning
    b64 = base64.b64encode(file_buffer.read()).decode()
    # return f'<a href="data:application/zip;base64,{b64}" download="{filename}.zip">{link_description}</a>'
    return f'<a href="data:{file_type};base64,{b64}" download="{filename}">{link_description}</a>'

def create_zip_memory(files):
    """Given list of files, returned buffer object containing a zipped file 
    
    Args: 
        files: list of files 
    """
    
    # Create a BytesIO buffer to hold the zip file
    buf = BytesIO()
    
    with zipfile.ZipFile(buf, 'w') as zipf:
        
        for filename, file_content in files.items():
            
            # Ensure the BytesIO object is at the start
            file_content.seek(0)
            
            # Read the content of the BytesIO object
            zipf.writestr(filename, file_content.read())
            
    buf.seek(0)
    
    return buf

def plot_time_series(chosen_dataset): 
    """Given the option chosen, plots a time series (scrollable and static) for all datasets or just one. 
    Renders 'Download CSV files' link and 'Download Time Series' link. 
    
    Args: 
        chosen_dataset: a string that can be either of "TRACE", "FAMOUS", "LOVECLIM", "All"    
    """
    
    dataset, time = load_datasets(chosen_dataset)
    if chosen_dataset == 'All': 
        plot_scrollable_series(dataset, time)
        csvs, img_buffer = plot_graph_time_series(dataset, time)

    else: 
        dataset = chosen_dataset.upper()
        plot_a_scrollable_series(dataset, dataset, time)
        csvs, img_buffer = plot_a_graph_time_series(dataset, dataset, time)
        
    # Generate zipped file with time series CSVs  
    zipped_buffer = create_zip_memory(csvs)

    # Generate link to download CSVs as zipped file 
    download_url = create_download_link(zipped_buffer, 'csv files', 'Download CSV files')
    st.markdown(download_url, unsafe_allow_html=True)

    # Generate link to download image of static time series plot
    img_download_url = create_download_link(img_buffer, 'plot.png', 'Download Time Series', file_type='image/png')
    st.markdown(img_download_url, unsafe_allow_html=True)

if generate: 
    plot_time_series(chosen_dataset)


