# Risk Factor Heat Maps

This repo provides python code to enable making heat maps of 29 different risk factors, health outcomes, and healthy behaviors utilizing data from the [CDC PLACES Project](https://www.cdc.gov/places/index.html). The code allows the flexibility to graph any number of the available data columns at either the state or county level, providing granularity at the Census Tract level. Some examples are provided in the root images folder. Below, a heat map is shown for Montgomery County, Maryland, showing the prevalence of Hypertension.

![Alt Text](https://github.com/razalamb1/risk-viz/blob/main/images/Maryland_Montgomery_Hypertension.png?raw=True)

This code utilizes the SODA API framework to pull the data as it is requested, and then merges with 2015 Census boundaries to produce the heat maps.

## Getting Started

If you would like to utilize this code locally, follow the steps below.

**Step 1: Clone the repo.**
```
git clone https://github.com/razalamb1/risk-viz.git
```

**Step 2: Navigate your way into the repo.**
```
cd risk-viz
```

**Step 3: Run the Makefile to install and/or update requirements.**
```
make install
```

**Step 4: Obtain API Keys for Socrata.**

Although an API key is not absolutely necessary for this code to run, it will make it signicantly faster. To obtain an API key, make an account with [Socrata](https://chronicdata.cdc.gov/signup). Then you will need to create a `.env` file with this API keys in the root directory, following the format from [the provided example](.env_example).

**Step 5: Add Necessary Census Data.**

To properly utilize this data, you will need the Census tract boundaries from 2015 in GeoJSON format. This data can be downloaded from this [Google Drive Folder](https://drive.google.com/drive/folders/1rguLCCqAliTArC74PJMhCKYDJv-KS74S?usp=sharing). Download this folder, and place it in the root directory of the cloned repo.

**Step 6: Write Code for Heap Maps.**

In order to use the code to generate your own heat maps, write python scripts in the root directory of the repo, similar to the [example](example.py). This style of code will generate images into the images folder.

**Author**: [Raza Lamb](https://github.com/razalamb1)



