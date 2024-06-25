## Region of Interest selector

# Instructions
- Run `python selector.py` or double click `run.command` on mac
- Click "Load Image" button and select the file you want to view for cropping
  - This assumes that the folder containing the file includes all other channels e.g. :
``` 
OC_Images
│   G1 Ano_3ng RANKL_stack_adj_A.jpg <-- open this file
│   G1 Ano_3ng RANKL_stack_adj_B.jpg
|   G1 Ano_3ng RANKL_stack_adj_G.jpg
|   G1 Ano_3ng RANKL_stack_adj_Y.jpg  
```

- Select all Regions of Interest by dragging
- Click "Save and Crop All" and select a folder to save the selections into
  - Better to create an empty folder for now, will implement adding to existing folder later
  - Selecting the folder will output as shown:
``` 
SelectedRegions
│   RoI_coordinates.json    
│
└───RoI1
|   |   G1 Ano_3ng RANKL_stack_adj_A.jpg
│   │   G1 Ano_3ng RANKL_stack_adj_B.jpg
|   |   G1 Ano_3ng RANKL_stack_adj_G.jpg
|   |   G1 Ano_3ng RANKL_stack_adj_Y.jpg  
│   
└───RoI2
|   |   G1 Ano_3ng RANKL_stack_adj_A.jpg
│   │   G1 Ano_3ng RANKL_stack_adj_B.jpg
|   |   G1 Ano_3ng RANKL_stack_adj_G.jpg
|   |   G1 Ano_3ng RANKL_stack_adj_Y.jpg  

...
```