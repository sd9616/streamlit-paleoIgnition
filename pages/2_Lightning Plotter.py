import matplotlib.pyplot as plt 
import streamlit as st
import numpy as np
import os
import pandas as pd
import plotly.express as px


lat_point = st.number_input('Latitude Point', 0, 360)
lon_point = st.number_input('Longitude Point', 0, 360)


project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print(project_path)

file_path = os.path.join(project_path, 'data')

TRACE = "TRACE"
FAMOUS = "FAMOUS"
LOVECLIM = "LOVECLIM"

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


# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

data = {}
data_frames = []
for key, dataset_files in dataset_files_list.items():
    var = dataset_files[0]
    lat = dataset_files[1]
    lon = dataset_files[2]
    
    lat_idx = np.argmin(np.abs(lat - lat_point))
    lon_idx = np.argmin(np.abs(lon - lon_point))

    # st.line_chart(time, var[:, lat_idx, lon_idx].flatten(), label=f'{key}')

    selected_frame = var[:, lat_idx, lon_idx].flatten()
    
    data_frames.append(pd.DataFrame({
    'lightning': selected_frame,
    'time': time,
    'dataset': key
    }))

# Combine all data frames into one
combined_data = pd.concat(data_frames, ignore_index=True)

fig = px.line(combined_data, x='time', y='lightning', color='dataset', title='Time vs Lightning')

fig.update_traces(showlegend=True)

fig.update_layout(xaxis_title='Time', yaxis_title='Lightning')
st.plotly_chart(fig, use_container_width=True)
    
#     # numpy_array = np.concatenate(time, var[:, lat_idx, lon_idx])
#     data[key] = pd.DataFrame({
#         'lightning': selected_frame, 
#         'time': time
#     })
#     # plot_data = list(zip(time, selected_frame))
    
#     print(f"key: {key}, shape: {np.shape(selected_frame)}")
#     # data[key] = plot_data
#     # print(np.shape(time))
#     # st.line_chart(numpy_array)


# # fig = px.line(stock, x="lightning", y="time", color_discrete_sequence=["#0514C0"], labels={'y': 'time'})
# # fig = px.line(data['TRACE'], x="time", y="lightning", color_discrete_sequence=["#0514C0"], labels={'y': 'Stock'})

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
    
    
# # ax.set_xlabel('Time')
# # ax.set_ylabel('Lightning')
# # ax.set_title(f'Time series of Lightning at Lat: {lat_point}, Lon: {lon_point}')
# # ax.grid(True)
# # ax.legend()
# # plt.tight_layout()

# # st.pyplot(fig)


# # Construct the absolute path to file



# # Close the plot to prevent memory leaks
# plt.close()
