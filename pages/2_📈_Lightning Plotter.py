import json
import matplotlib.pyplot as plt 
import streamlit as st
import numpy as np
import os
import pandas as pd
import plotly.express as px


st.markdown("""
            ## Lightning Time Series Plotter
            """)

# Select a Dataset
chosen_dataset = st.selectbox(
    "Pick a Dataset to plot or choose all!",
    ("TraCE", "FAMOUS", "LOVECLIM", "All"))

# Enter lat and Lon
lat_point = st.number_input('Latitude Point (between -90 and 90)', -90, 90)
lon_point = st.number_input('Longitude Point (between 0 and 360)', 0, 360)

# Hit generate
col1, col2, col3, col4 = st.columns([0.20, 0.65, 0.1, 0.15])

generate = col1.button("Generate", type="primary")
    
project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(project_path)

file_path = os.path.join(project_path, 'data')

TRACE = "TRACE"
FAMOUS = "FAMOUS"
LOVECLIM = "LOVECLIM"


# Returns a dictionary with each dataset constant as the key and a array of time 
# (dataset_dict, time)
def load_datasets(): 
    # [variable, latitude, longitude, time]
    dataset_files_loveclm = [
        np.load(os.path.join(file_path, 'lc_rolling_avg_trimmed.npy')),
        np.load(os.path.join(file_path, 'lc_lat.npy')),
        np.load(os.path.join(file_path, 'lc_lon.npy'))
    ]

    dataset_files_trace = [
        np.load(os.path.join(file_path, 'tr_rolling_avg_trimmed.npy')),
        np.load(os.path.join(file_path, 'tr_lat.npy')),
        np.load(os.path.join(file_path, 'tr_lon.npy'))
    ]

    dataset_files_famous = [
        np.load(os.path.join(file_path, 'fa_rolling_avg_trimmed.npy')),
        np.load(os.path.join(file_path, 'fa_lat.npy')),
        np.load(os.path.join(file_path, 'fa_lon.npy'))
    ]

    time = np.load(os.path.join(file_path, 'time_rolling_21_0.4.npy'))

    dataset_files_list = {
        TRACE: dataset_files_trace,
        LOVECLIM: dataset_files_loveclm,
        FAMOUS: dataset_files_famous,
    }
    
    return dataset_files_list, time
    
def plot_scrollable_series(): 
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 6))

    data_set = []
    data_frames = []

    datasets, time = load_datasets()

    for key, dataset_files in datasets.items():
        var, lat, lon = dataset_files
        
        lat_idx = np.argmin(np.abs(lat - lat_point))
        lon_idx = np.argmin(np.abs(lon - lon_point))

        # st.line_chart(time, var[:, lat_idx, lon_idx].flatten(), label=f'{key}')

        selected_frame = var[:, lat_idx, lon_idx].flatten()
        
        df = pd.DataFrame({
                                        'lightning': selected_frame,
                                        'time': time,
                                        'dataset': key
        })
        data_frames.append(df)
        
        print(f"{np.shape(time)}, {np.shape(selected_frame)}")
        data = np.column_stack((time, selected_frame))

        np.savetxt(os.path.join(project_path, f"{key}.csv"), data, delimiter=',')
        
    # Combine all data frames into one
    combined_data = pd.concat(data_frames, ignore_index=True)

    # fig = px.line(combined_data, x='time', y='lightning', color='dataset', title=f'Time series of lightning at {lat_point}, {lon_point}')

    # fig.update_traces(showlegend=True)

    # fig.update_layout(xaxis_title='Time (kaBP)', yaxis_title='Lightning (mm/day)')
    # st.plotly_chart(fig, use_container_width=True)
    fig = px.line(combined_data, x='time', y='lightning', color='dataset',
                title=f'Time series of lightning at {lat_point}, {lon_point}',
                labels={'time': 'Time (kaBP)', 'lightning': 'Lightning (mm/day)'},
                color_discrete_map={'TRACE': 'blue', 'FAMOUS': 'green', 'LOVECLIM': 'orange'})

    fig.update_traces(mode='lines', showlegend=True)

    fig.update_layout(xaxis_title='Time (kaBP)', yaxis_title='Lightning (mm/day)')
    st.plotly_chart(fig, use_container_width=True)

    
def plot_graph_time_series():
    
    plt.figure(figsize=(10, 6))

    datasets, time = load_datasets()
    for key, dataset_files in datasets.items():
        var, lat, lon = dataset_files

        lat_idx = np.argmin(np.abs(lat - lat_point))
        lon_idx = np.argmin(np.abs(lon - lon_point))

        if lat_idx < 0 or lat_idx >= lat.shape[0] or lon_idx < 0 or lon_idx >= lon.shape[0]:
            st.write(f"Error: Latitude or longitude values are out of bounds for the dataset {key}. Skipping.")
            continue

        plt.plot(time, var[:, lat_idx, lon_idx].flatten(), label=f'{key}')

    plt.xlabel('Time')
    plt.ylabel('Lightning')
    plt.title(f'All Datasets: Time series of Lightning at {lat_point}, {lon_point}')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    
    # Display the plot using Streamlit
    st.pyplot(plt)

    # Close the plot to prevent memory leaks
    plt.close()

#     fig, ax = plt.subplots(figsize=(10, 6))

#     data = {}
#     data_frames = []

#     datasets, time = load_datasets()

#     for key, dataset_files in datasets.items():
#         var = dataset_files[0]
#         lat = dataset_files[1]
#         lon = dataset_files[2]
        
#         # print(f"Lat range {max(lat)}, {min(lat)}")
#         # print(f"Lon range {max(lon)} {min(lon)}")
        
#         lat_idx = np.argmin(np.abs(lat - lat_point))
#         lon_idx = np.argmin(np.abs(lon - lon_point))

#         # st.line_chart(time, var[:, lat_idx, lon_idx].flatten(), label=f'{key}')

#         selected_frame = var[:, lat_idx, lon_idx].flatten()
        
#         # data_frames.append(pd.DataFrame({
#         #                                 'lightning': selected_frame,
#         #                                 'time': time,
#         #                                 'dataset': key
#         # }))
# #     # numpy_array = np.concatenate(time, var[:, lat_idx, lon_idx])
#         data[key] = pd.DataFrame({
#             'lightning': selected_frame, 
#             'time': time
#         })
#     # plot_data = list(zip(time, selected_frame))
    
#     print(f"key: {key}, shape: {np.shape(selected_frame)}")
#     # data[key] = plot_data
#     # print(np.shape(time))
#     # st.line_chart(numpy_array)


    # fig = px.line(stock, x="lightning", y="time", color_discrete_sequence=["#0514C0"], labels={'y': 'time'})
    # fig = px.line(data['TRACE'], x="time", y="lightning", color_discrete_sequence=["#0514C0"], labels={'y': 'Stock'})

    # fig = px.line(data['TRACE'], x="time", y="lightning", title='Trace')
    # fig = px.line(data['FAMOUS'], x="time", y="lightning", title='Famous')
    # fig = px.line(data['LOVECLIM'], x="time", y="lightning", title='Loveclim')

    # fig.update_layout(title='Time vs Lightning', xaxis_title='Time', yaxis_title='Lightning')
    # fig.show()
    

# st.plotly_chart(fig, use_container_width=True)


# # data_dict = {key: plot_data for key, plot_data in data}

# # chart_data = pd.DataFrame(data)

# # print(data)
# # for key, plot_data in data_dict.items(): 
# # st.line_chart(chart_data)
    
    
# ax.set_xlabel('Time')
# ax.set_ylabel('Lightning')
# ax.set_title(f'Time series of Lightning at Lat: {lat_point}, Lon: {lon_point}')
# ax.grid(True)
# ax.legend()
# plt.tight_layout()

    # st.pyplot(fig)


# # Construct the absolute path to file



# # Close the plot to prevent memory leaks
# plt.close()

# Create a download button

        
def plot_time_series(chosen_dataset): 
    
    if chosen_dataset == "All": 
    
        plot_scrollable_series()
        plot_graph_time_series()
        
        
    with col3: 
        
        st.button("CSV")
        
    with col4: 
        st.button("Graph")
    
    # col1.button()
    
if generate: 
    plot_time_series(chosen_dataset)
