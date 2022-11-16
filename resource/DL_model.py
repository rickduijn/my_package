import roboflow

# Instantiate Roboflow object with your API key
rf = roboflow.Roboflow(api_key='wptrChO5R7M43Ga9QRi9')

# List all projects for your workspace
workspace = rf.workspace()

# Load a certain project, workspace url is optional
project = rf.workspace("wageningen-university").project("post_trunk_15-11")

# List all versions of a specific project
project.versions()

# Upload image to dataset
project.upload("image.jpg")

# Retrieve the model of a specific project
model = project.version("1").model

# predict on a local image
prediction = model.predict("image.jpg")

# Predict on a hosted image
#prediction = model.predict("YOUR_IMAGE.jpg", hosted=True)

# Plot the prediction
prediction.plot()

# Convert predictions to JSON
prediction.json()

# Save the prediction as an image
prediction.save(output_path='predictions.jpg')