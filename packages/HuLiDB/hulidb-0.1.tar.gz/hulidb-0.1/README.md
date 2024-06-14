# HuLiDB: Synthetic Hub-mounted Lidar Database

The HuLiDB repository, developed in Python v3.9, facilitates the extraction of hub-lidar configuration measurements from NetCDF4 files. Each file corresponds to a specific inflow condition, characterized by wind speed, seed, and turbulence intensity. The data originate from a hub-lidar sensor simulation in [HAWC2 v13.1](https://www.hawc2.dk/), a single-beam wind pulsed lidar mounted on the hub/spinner of the wind turbine model. For detailed specifications of the hub-lidar sensor in HAWC2, see the [documentation](https://findit.dtu.dk/en/catalog/6580a4d96063f329d3040be8).

Download the **HuLiDB** database from [DTU Data](https://data.dtu.dk/articles/dataset/_b_Numerical_hub-lidar_data_from_Mann-generated_b_b_turbulence_boxes_using_HAWC2_v13_1_and_DTU_10MW_b_b_reference_wind_turbine_b_/23904990). For comprehensive details on generation processes, inflow conditions, and configurations, refer to the official dataset document: [Numerical hub-lidar data from Mann-generated turbulence boxes using HAWC2 v13.1 and the DTU 10MW reference wind turbine](https://gitlab.windenergy.dtu.dk/continue/hublidardatabase/-/blob/main/CONTINUE_HuLiDatabase.pdf?ref_type=heads).

The toolbox enables users to:

-   Create their own dataset using custom configurations and Mann-turbulence boxes via [HAWC2 v13.1](https://www.hawc2.dk/).
-   Extract aeroelastic simulation data from the DTU 10MW reference wind turbine under selected inflow conditions.
-   Retrieve synthetic measurements from various hub-mounted lidar configurations for the specified inflow conditions.

This dataset is part of the [CONTINUE (Control of next-generation wind turbines)](https://eudp.dk/en/node/16680) project, curated by Esperanza Soto Sagredo (ORCID 0000-0002-5645-2335, espa@dtu.dk) and Jennifer M. Rinker (ORCID 0000-0002-1122-1891, rink@dtu.dk) at the Technical University of Denmark using [HAWC2 v13.1](https://www.hawc2.dk/). The project is funded by the Danish Energy Technology Development and Demonstration Programme ([EUDP](https://eudp.dk/en)), under grant agreement 64022-496980.

## HuLiDB Installation

To utilize the **HuLiDB** toolbox, it is advisable to set up a new environment using Python v3.9:

	conda create --name env_name python=3.9
	conda activate env_name

This environment should be equipped with specific packages to ensure compatibility and performance.

### Requirements

- [Numpy, version 1.23.5](https://numpy.org/)
- [Pandas, version 1.5.3](https://pandas.pydata.org/)
- [Matplotlib, version 3.7.0](https://matplotlib.org/)
- [netCDF4, version 1.6.3](https://pypi.org/project/netCDF4/)
- [xarray, version 2023.4.2](https://docs.xarray.dev/en/stable/)
- [Wind Energy Tool box, version 0.1.0](https://toolbox.pages.windenergy.dtu.dk/WindEnergyToolbox/)
- [Scipy, version 1.10.0](https://scipy.org/install/)

To install these dependencies, execute the following commands:

	# Install Numpy:
	python -m pip install "numpy==1.23.5"
	
	# Install Pandas:
	python -m pip install "pandas==1.5.3"
	
	# Install Matplotlib:
	python -m pip install "matplotlib==3.7.0"

	# Install netCDF4: 
	python -m pip install "netcdf4==1.6.3"
	
	# Install xarray:
	python -m pip install "xarray==2023.4.2"
	
	# Install the Wind Energy Tool Box (wetb): 
	python -m pip install "wetb==0.1.0"

	# Install Scipy:
	python -m pip install "scipy==1.10.0"
	
After setting up the environment and installing the required packages, you can clone the **HuLiDB** toolbox to your preferred directory and start utilizing it from your newly created environment:

	git clone https://gitlab.windenergy.dtu.dk/continue/hublidardatabase.git

## Repository Architecture
This repository is structured as follows:
<pre>
    hublidardatabase
    ├───dtu_10mw
    │   ├───control
    │   ├───data
    │   ├───htc
    ├───files
    ├───hulidb
    │   └───data_extraction.py
    │   └───database_generation.py
    │   └───functions.py
    │   └───functions_NETcdf.py
    │   └───functions_tbox.py
    │   └───lidar_utilities.py
    │   └───turbox.py
    ├───NETcdf
    │   └─── Save the NetCDF files from DTU Data in this folder
    ├───.gitignore
    ├───_ltb_values.py
    ├───_var_names.py 
    ├───01-make_htc_files.py
    ├───02-add_shear_tbox.py
    ├───03-NETcdf_generation.py
    ├───04-Data_extraction.py  
    ├───CONTINUE_HuLiDatabase.pdf
    ├───LICENSE
    ├───README.md
</pre>

Folders details: 

-  $\textcolor{blue}{\text{dtu\_10mw}}$: Houses the DTU10MW reference wind turbine model used in database generation, including controller's files, operational data, and HAWC2 htc files.
	- $\textcolor{blue}{\text{\textbackslash htc}}$: Contains three subfolders:
		- $\textcolor{blue}{\text{lidar\_simulation}}$: Stores htc files for hub-lidar data extraction
		- $\textcolor{blue}{\text{turb\_box}}$: Contains htc files for generating Mann turbulence boxes in HAWC2. These must be run first to generate turbulence boxes, followed by simulation files in $\textcolor{blue}{\text{lidar\_simulation}}$ for data extraction.
		- $\textcolor{blue}{\text{free\_wind}}$: Includes files to analyze free wind components u, v, and w at different positions within the turbulence box from HAWC2.
- $\textcolor{blue}{\text{files}}$: This directory contains the spreadsheet $\textcolor{purple}{\text{Lidar\_beams\_hawc2.csv}}$, detailing all available configurations for data extraction based on the dictionary $\textcolor{blue}{\text{lidar\_arg}}$ in $\textcolor{blue}{\text{\_ltb\_values.py}}$. This file should remain unaltered.
- $\textcolor{blue}{\text{hulidb}}$: Hosts several Python scripts with utility functions for the repository, organized by function.
- $\textcolor{blue}{\text{NETcdf}}$: Designated for storing NetCDF4 files downloaded from [DTU Data](https://data.dtu.dk/articles/dataset/_b_Numerical_hub-lidar_data_from_Mann-generated_b_b_turbulence_boxes_using_HAWC2_v13_1_and_DTU_10MW_b_b_reference_wind_turbine_b_/23904990). You may download only the inflow cases relevant to your needs. Each file is approximately 10.75 GB in size.

# Repository Instructions

This repository enables you to [generate your own dataset](#database-generation) or [extract data from an existing database](#data-extraction-from-netcdf-files), using the NetCDF files available at [DTU Data](https://data.dtu.dk/articles/dataset/_b_Numerical_hub-lidar_data_from_Mann-generated_b_b_turbulence_boxes_using_HAWC2_v13_1_and_DTU_10MW_b_b_reference_wind_turbine_b_/23904990).

## Database generation 

This section details the purpose and usage of the scripts in this repository, primarily for creating your own dataset using [HAWC2 v13.1](https://www.hawc2.dk/).

#### Dictionary for Generation and Data Extraction: _ltb_values.py

This script contains five dictionaries essential for:

- $\color{blue} \text{kw\_dtu10mw}$: Provides values for the DTU 10MW reference wind turbine model in HAWC2, including the index of output channels for simulations.
- $\color{blue} \text{kw\_turbgen}$: Specifies parameters for generating Mann turbulence boxes.
- $\color{blue} \text{lidar\_arg}$: Includes values for selecting hub-mounted lidar configurations to be added to the output channels in HAWC2.
-   Two additional dictionaries are defined for test cases.

### Variable Name Definition and Metadata: _var_names.py

This script holds the metadata definitions for generating the NetCDF file, covering all data types including the aeroelastic response of the wind turbine model, hub-lidar data across multiple beams, and Mann-generated turbulence boxes.


### Script 01-make_htc_files
This script is dedicated to generating the necessary htc files for simulations in the following scenarios:

- **Generation of Mann-turbulence boxes (wind-inflow conditions):** Files will be saved within the folder $\textcolor{blue}{\text{dtu\_10mw\textbackslash htc\textbackslash turb\_box\textbackslash}}$. It creates htc files for 10-second simulations, exclusively for generating the required turbulence boxes. **Note**: These files must be executed first to provide the inflow necessary for subsequent simulations.
- **Aeroelastic simulations for hub-lidar measurement generation/extraction:** Files are stored in $\textcolor{blue}{\text{dtu\_10mw\textbackslash htc\textbackslash lidar\_simulations\textbackslash}}$. Due to output channel constraints in HAWC2, a maximum of 2000 beams per file is set, resulting in 18 htc files per inflow condition depending on the number of hub-lidar beam output sensors required, as defined in the dictionary $\color{blue} \text{lidar\_arg}$.
- **Optional extraction of free wind components u, v, and w:** A htc file can be generated to analyze the wind speed components at each timestep in HAWC2, stored under $\textcolor{blue}{\text{dtu\_10mw\textbackslash htc\textbackslash free\_wind\textbackslash}}$.

The htc files are based on a template located at $\textcolor{blue}{\text{dtu\_10mw\textbackslash htc\textbackslash DTU\_10MW\_orig\_v2.htc}}$, 
containing the main output channels and format for the DTU 10 MW reference wind turbine. All simulations by default use a flexible tower and a 5-degree tilt, though these settings can be adjusted in the function $\color{blue}\text{make\_htc\_turb}$.

The code customizes htc files for various inflow conditions with the following parameters:

-   Wind speeds and seed numbers as specified in $\textcolor{blue}{\text{\_ltb\_values.py --> kw\_turbgen}}$. 
- Beam lidar configurations stored in the DataFrame $\color{blue} df\_lidar$, based on initial values from $\textcolor{blue}{\text{\_ltb\_values.py --> lidar\_arg}}$.
-   Mann turbulence box parameters, with $\alpha \epsilon ^{2/3}$ calculated using the function $\color{blue}var2ae$ from the [WETB tool box](https://toolbox.pages.windenergy.dtu.dk/WindEnergyToolbox/), and parameters $\color{blue}L$ and $\color{blue}\Gamma$ selected from the dictionary in $\textcolor{blue}{\text{\_ltb\_values.py --> kw\_turbgen}}$. Refer to the [database documentation](https://gitlab.windenergy.dtu.dk/continue/hublidardatabase/-/blob/main/CONTINUE_HuLiDatabase.pdf?ref_type=heads) for detailed information on turbulence box generation and required parameters.

Due to memory constraints during simulation, the htc files limit the number of beams to $\color{blue} beamno\_htc$ = 2000 beams per file. Surpassing this number significantly increases the processing time required by HAWC2 for output channels.

For each inflow condition, multiple htc files are generated based on the total number of beam configurations selected and the maximum number of beam outputs per file ($\color{blue} beamno\_htc$). The total number of simulations or parts is calculated by dividing the total number of output beams required (based on the lidar configurations combinations from $\textcolor{blue}{\text{\_ltb\_values.py --> lidar\_arg}}$) by the maximum number of beams per file.

### Script 02-add_shear_tbox

This script processes each Mann-generated turbulence box, adding a shear profile to the longitudinal component u. It employs a power law with a shear exponent of 0.2 to modify the u component. The modified data is then saved as a binary file in the HAWC2 format, which is subsequently utilized in the aeroelastic simulations within HAWC2.

**Note:** The addition of the shear profile is not conducted using HAWC2’s default shear option. This approach is necessary because the center of the turbulence box does not coincide with the hub height of the wind turbine model in HAWC2, which uses the vertical center of the turbulence box as the reference height for applying the shear profile.

### Script 03-NETcdf_generation

This script processes results from each inflow case derived from HAWC2 aeroelastic simulations, and compiles them into a NetCDF4 file specific to each inflow scenario.

The naming convention for the files is as follows:

	[name_wind_turbine_model]_wsp_[wsp]_seed_[seed_number]_ae_[ae_value]

The generated NetCDF files are structured into three groups:

- ***wt_res***: This group contains the output channels from the aeroelastic wind turbine response in HAWC2. For details about these output channels, refer to the documentation: [Numerical hub-lidar data from Mann-generated turbulence boxes using HAWC2 v13.1 and the DTU 10MW reference wind turbine](https://gitlab.windenergy.dtu.dk/continue/hublidardatabase/-/blob/main/CONTINUE_HuLiDatabase.pdf?ref_type=heads).
- ***HuLi_data***: This group holds all the lidar beams data, including the global coordinates (Xg, Yg, Zg) and both nominal and weighted line-of-sight velocities for all selected beams.
- ***mann_tbox***: This group encompasses the Mann-generated turbulence box for the specific inflow case. It includes components u, v, w, and u_shear (the u component with an added power law shear profile), structured under the meteorological coordinate system dimensions (x, y, z). Additionally, the time as HAWC2 processes the turbulence box is recorded. For more information, please consult [Section 5. Numerical HuLi dataset](https://gitlab.windenergy.dtu.dk/continue/hublidardatabase/-/blob/main/CONTINUE_HuLiDatabase.pdf?ref_type=heads).

## Data extraction from NetCDF files

This section provides guidance on using the repository to extract desired data from the NetCDF files, based on specific hub-lidar configurations chosen by the user. The data can be extracted from three different $\color{blue} groups$ as outlined in the [previous section](#script-03-netcdf_generation).

**Note:** Each NetCDF file for an inflow case is approximately 10.76 GB in size. Extracting data for specific hub-lidar configurations may take between 1 to 5 minutes, varying with the number of beams, configurations selected, and computer performance.

### Script 04-Data_extraction

This script is crucial for users as it reads the NetCDF4 files for one or multiple inflow cases, extracting data from the aeroelastic response, hub-lidar measurements based on user-defined configurations, and the Mann-turbulence box.

#### $\color{blue} \text{a) Extraction of aeroelastic response of the wind turbine:}$

To extract the **aeroelastic response of the wind turbine**, the script generates and saves the dictionary `df_aero` as a pickle file. This file will contain all the aeroelastic responses across multiple inflow cases, located on the list `Cases`:

	# Cases to be evaluated based on dict kw_turgen:
	# Cases = fNet.generate_Cases(**kw_turbgen)
	 
	# Cases based on the available NetCDF4 files in folder ./NETcdf/
	# It will check the folder, and look for all files with extension .nc
	Cases = func.check_files_and_convention(folder_path)
	path = './NETcdf/'  # Path where netcdf files are saved.
	path_to_save = './files/'    # Path to save the pickle file
	fname = 'df_aero'  # Name of the file to be saved for aeroelastic response as pickle format.
	
	# Generates a nested dataframes in a dictionary df_aero, with aeroelastic response for each inflow case. 
	# save=True will save the dictionary into a pickle file. This is optional.
	df_aero = dext.extract_aero_resp(Cases, path, path_to_save=path_to_save, fname=fname, save=True)

An example of the `df_aero[case]` dataframe, where `case` is the name of the inflow case, is shown:

	         Time  shaft_rot_angle  ...  DLL_pitch3  DLL_Bld_tip_tow
	0      100.05       166.518173  ...    0.003150        29.396481
	1      100.10       168.386520  ...    0.003168        27.913652
	2      100.15       170.254868  ...    0.003189        26.606422
	3      100.20       172.117737  ...    0.003212        25.491051
	4      100.25       173.986069  ...    0.003237        24.587046
	      ...              ...  ...         ...              ...
	11995  699.80       270.934814  ...   -0.000000        44.363602
	11996  699.85       273.294373  ...   -0.000000        41.660835
	11997  699.90       275.659393  ...   -0.000000        38.967415
	11998  699.95       278.018921  ...   -0.000000        36.294376
	11999  700.00       280.378479  ...   -0.000000        33.671452

	[12000 rows x 120 columns]

For additional details on the aeroelastic response output channels, please refer to [appendix A in the documentation](https://gitlab.windenergy.dtu.dk/continue/hublidardatabase/-/blob/main/CONTINUE_HuLiDatabase.pdf?ref_type=heads).

#### $\color{blue} \text{b) Extraction of Hub-Lidar Measurements:}$

To extract hub-lidar measurements based on specific lidar configurations, define each configuration individually and compile them into a list as shown below:

	# Definition of selected configurations (This is an example with two configs.):

	# Configuration 1: Five beam lidar configuration, with 28 ranges
	config_1 = {'theta': [0, 20, 30, 30, 30],  # Half-cone angle
	            'psi': [0, 60, 120, 180, 240],  # Azimuthal angle
	            'Focus-Length': np.concatenate((np.arange(50, 200, 10), 
	                                      np.arange(200, 505, 25))),
	            }

	# Configuration 2: One beam lidar configuration, with 10 ranges
	config_2 = {'theta': [0],  # Half-cone angle
	            'psi': [0],
	            'Focus-Length': np.arange(50, 310, 10),
	            }

	# Final list with all the configurations to be extracted: 
	lidar_config = [config_1, config_2]

Additionally, specify parameters such as the sampling frequency per beam in Hz, the desired time interval for data extraction, and the timestep for outputs from HAWC2 (`deltat = 0.05 [s]`). The extraction should start at a minimum time of `t_start = 100.05` seconds and can continue up to `t_end = 700` seconds. The `deltat` value is specified in the output section of the HAWC2 htc file, set to 0.05 seconds for this database.

	sampling_freq = 5  # [Hz] per beam
	t_start, t_end = 100.05, 700.05  # This time is also constrained as the available time from HAWC2 simulation
	deltat = 0.05   # delta time from HAWC2 simulation output channels.

The sampling frequency per beam dictates the data sampling and extraction from HAWC2 results files. The total full scan time is determined by multiplying the sampling frequency per beam by the number of beams in a configuration. **No switching delay is accounted for**.

To generate the nested dictionary `DF_lidar`, which contains dataframes for each inflow and configuration case, use the following function:

	# Extract Hub-lidar data and generates a dictionary with the extracted data:
	DF_lidar = dext.extract_huli_data(Cases, df_lidar, lidar_config, 
	                                sampling_freq, t_start, t_end, deltat,
	                                path=path_to_save, fname=file_name, save=True)

Where `df_lidar` is a dataframe that imports all output beams from the dataset generation and can be accessed through **.\files\Lidar_beams_hawc2.csv**:

	lidar_csv = ('.\\files\\Lidar_beams_hawc2.csv')
	df_lidar = pd.read_csv(lidar_csv)
	df_lidar = df_lidar.drop(['Unnamed: 0', 'Beggining', 'Tag'], axis=1)

**Note**: The file **.\files\Lidar_beams_hawc2.csv** should not be modified. However, if necessary, it can be regenerated with:

	df_lidar = create_lidar_config_htc(kw_dtu10mw['z_hub'], lidar_arg)

Below is an example of the generated dataframe `DF_lidar` for one inflow case, specifically for configuration 1:
	
	# Example for DF_lidar[case]['config_1']:
	
	         Time  shaft_rot_angle  hub1_pos_x  ...  Theta  Psi  Beam_No
	0      100.05       166.518173   -0.026284  ...      0    0       b1
	1      100.05       166.518173   -0.026284  ...      0    0       b1
	2      100.05       166.518173   -0.026284  ...      0    0       b1
	3      100.05       166.518173   -0.026284  ...      0    0       b1
	4      100.05       166.518173   -0.026284  ...      0    0       b1
	      ...              ...         ...  ...    ...  ...      ...
	16795  699.85       273.294373   -0.058121  ...     30  240       b5
	16796  699.85       273.294373   -0.058121  ...     30  240       b5
	16797  699.85       273.294373   -0.058121  ...     30  240       b5
	16798  699.85       273.294373   -0.058121  ...     30  240       b5
	16799  699.85       273.294373   -0.058121  ...     30  240       b5

	[84000 rows x 13 columns]

For further details on the output data, please consult [Section 5 of the Numerical HuLi dataset documentation](https://gitlab.windenergy.dtu.dk/continue/hublidardatabase/-/blob/main/CONTINUE_HuLiDatabase.pdf?ref_type=heads).

#### $\color{blue} \text{c) Extraction of Mann-generated turbulence boxes}$

To extract the Mann-turbulence boxes, use the function $\color{blue} \text{extract\_tbox\_from\_netcdf}$ which will extract the data and save it as HAWC2 binary files. This includes four files: **u, v, w,** and **u_shear**, where **u_shear** is the longitudinal wind component **u** with an added shear profile, generated by script $\color{blue} \text{02-add\_shear\_tbox.py}$. The naming convention follows that of the inflow case:

	# To extract Turbulence box in HAWC2 binary file (four binary files generated):
	path_netcdf = './NETcdf/'  # Path where the NetCDF file is located.
	path_turb_save = './dtu_10mw/turb_saved/'  # Path to save the turbulence box values extracted.
	
	# if hawc2_file is True, then it generates the HAWC2 binary files. 
	dext.extract_tbox_from_netcdf(case, path_netcdf, path_turb_save, hawc2_file=True)

If the optional argument **hawc2_file** is set to false, the function will return the 3D arrays:

	# if hawc2_file is False, then it will return the u, v, w and u_shear as 3D arrays.
	u, v, w, u_shear = dext.extract_tbox_from_netcdf(case, path_netcdf, path_turb_save, hawc2_file=False)

## Acknowledgment

My deepest thanks go to my supervisors, Jennifer M. Rinker, Mike Courtney, and Ásta Hannesdóttir, for their unwavering support, guidance, and insightful feedback during the development of this database.

Special thanks to Rasmus Sode Lund for his significant contributions to implementing the numerical hub-lidar sensor in HAWC2 v13.1, which made the creation of this database possible.

This work is part of the CONTINUE project, which has received funding from the Danish Energy Technology Development and Demonstration Programme (EUDP), under grant agreement 640222-496980. 

## License

[MIT License](https://gitlab.windenergy.dtu.dk/continue/hublidardatabase/-/blob/main/LICENSE)

**© Copyright © 2024, Technical University of Denmark**
HuLiDB  was developed by Esperanza Soto Sagredo (espa@dtu.dk), PhD student, DTU Wind and Energy Systems.