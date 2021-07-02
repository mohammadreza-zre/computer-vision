optical character recocnition (OCR)

aim ---->> extracting personal and account information such as  1.account number  2.expiration date  3.owner name  4.bank name and  .... from credit cart

im this project we use python and opencv for extraction

steps contain :
              1 . loading image od cart
              2 . findig the region if intrest(ROI) in the main image by contours
              3 . (1) preprocessing on the cart for finding region of data on the cart - (2) on another way we can use the EAST algoritm for seeking ROIs automatically .
              4 . grab the sections that assume contain our information and draw rectangles for them 
              5 . pass the ROIs to the Tesseract algoritm and the algoritm return informations
              6 . detecting outputs and figure out the relation beetwen them and the type of information on the cart . for instance expiration data has a specific symptom for 
                  separating with other informations and that is -/- and all of them will recognize by one or more sympyom .
