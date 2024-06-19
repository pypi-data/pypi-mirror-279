### Install OpenMP
`brew install libomp`


### Ensure R (version above 3.5) is pre-installed
For linux, below steps can be followed for installation:
`sudo add-apt-repository 'deb https://cloud.r-project.org/bin/linux/ubuntu xenial-cran35/'`

`sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys E084DAB9`

`sudo apt update`

`sudo apt install r-base-dev`

### Configure token from 'mosaic-ai-backend'
Run the command in a separate terminal window
`curl \
  -o ~/.mosaic.ai \
  -X POST \
  -H 'X-Auth-Email: akhil.lawrence@lntinfotech.com' \
  -H 'X-Auth-Userid: akhil.lawrence' \
  -H 'X-Auth-Username: akhil.lawrence' \
  -H 'X-Auth-Groups':'[/mosaic/mosaic-ai-logistics]' \
  http://localhost:5000/registry/api/v1/token`

### clone repository
`git clone https://git.lti-aiq.in/mosaic-ai-logistics/mosaic-ai-client.git`

### install mosaic-ai-client
`cd mosaic-ai-client`

### create directory logs
`mkdir logs`

### create a blank log file
`touch logs/mosaic-ai-client.log`

### create a virtual environment
`virtualenv --python=/home/LNTINFOTECH/10671666/.pyenv/versions/3.7.0/bin/python3 env`

### activate environment
`source env/bin/activate`

### check pip version
`pip --version`

### Install mosaic-ai-client
`make install`

### Running application
`make run`

Once Jupyter opens up in the browser, select a notebook and run the steps to build and register the model. Save 'object-url' from the response of register_model(). The value will be used in setting up environment variables for 'mosaic-ai-serving'. In register_model() function, ensure that there is no '-' in the model name
