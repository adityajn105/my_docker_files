## Step to get you model trained to predict caption

#### 1. Install dependencies

* You can install all dependencies by using following command.

	> pip install -r requirements.txt


#### 2. Fetch data flicker 8k/30k and glove.6b.50d embeddings

* Use following command to fetch all required data using fetch_data.sh script. 
	
	> bash fetch_data.sh 8k

#### 3. Build all required protocol buffers

* Use build.sh to build all required python based protocol buffers
	
	> bash build.sh

#### 4. Finally train the model.

* It will use models defined in models.py and save it in format that will be used by tensorflow-serving api.

	> python train_and_save_model.py