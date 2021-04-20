# medical-chatbot

## Installation
    google-trans-new==1.1.9

## Usage

**1. Query Entity**  
The script to map given (intent,[entities]) is in `src/main.py`  

The extracted *Vietnamese KB* is in `cancer_data/final_kb.json`  

To extract enties:  
`python main.py [--q Query](boolean) [--s SemanticFrame](boolean) [--path_out Path](optional) [--i Intent] [--e Entites]`


Example: 
```     
python main.py --q True --i 'symptom' --e 'thalassemia' 'ung thư gan' 'buồn nôn'
```
Output:
```
thalassemia : mệt mỏi
thalassemia : không có triệu chứng
thalassemia : chỉ những người nhẹ
ung thư gan : giảm cân mà không cần cố gắng
ung thư gan : ăn mất ngon
ung thư gan : đau bụng trên
buồn nôn : ung thư gan
```
**2. Build KB**
All the scripts for KB are in `cancer_data/`  

There are 2 steps:   
1. Build english kb from file `data.json` to export `database.json`  
    ```python build_kb.py```
        
2. Build vietnamese kb . Output is `final_kb.json`   

    ```python translate.py```

**3. Get symptoms entities**   
```    
    cd src/  
    python utils.py
```

The output files are in : `symptoms_ent/` folder
## Future work
-   Entity Linking to enrich Vietnamese KB 
-   Argument inputs [x]
-   Ranking output 
-   Refactor [x]
-   Load balancer for KB access
