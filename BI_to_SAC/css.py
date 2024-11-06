round_button = """
<style>.element-container:has(#button-after) + div button {
    position: fixed;
    bottom: 20px;
    right: 20px;
    border-radius: 50%; 
    background-color: #262730; 
    color: white;
    padding: 5px 15px; 
    cursor: pointer; 
    height: 40px;
    width: 40px;
    border: none;
    font-size: 20px;
    overflow: hidden;
 }
 .element-container:has(#button-after) + div button:hover{
    box-shadow: 0px 0px 15px rgb(175,61,255);
    color: rgb(175,61,255);
 }
 </style>"""

edit_button = """
<style>.element-container:has(#button-edit) + div button {
    position: absolute;
    # bottom: 20px;
    right: 0px;
    background-color: #262730; 
    color: white;
    cursor: pointer; 
    # height: 20px;
    # width: 35px;
    border: none;
    font-size: 10px;
    overflow: hidden;
}
.element-container:has(#button-edit) + div button:hover{
    box-shadow: 0px 0px 15px rgb(175,61,255);
    color: rgb(175,61,255);
}
</style>""" 