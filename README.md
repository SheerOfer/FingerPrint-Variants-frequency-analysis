# FingerPrint | Variants frequency analysis
**Overview**


run "fingerprint_variants" to extract all variants from a given excel file.
* Remember to change file path in main!
* excel file need to be in the foramt: coulmns = patiants (ex 137Y), rows = vriants (ex 152TC).


* Create a new excel conaining all variants in the format {var:[patients with this var]}.
* Create very_common_variants dict containing all the patients missing one variant out of 6 most common variants.
	*  'M-263-A-G', 'M-750-A-G', 'M-1438-A-G', 'M-4769-A-G', 'M-8860-A-G', 'M-15326-A-G'.
* Given a patient number, get an excel file with all the variants showed count smaller then 500 (out of 61134 in the database), and all the frequencies for these variants according to mitomap.

Based on the "mitomap Look up Co-variants" tool - Compute frequencies of a variant with or without co-occurence with another variant. https://www.mitomap.org/cgi-bin/covariants


**Installation**
* Python 3.11 or higher
* Required Python packages:
 	* openpyxl
  	* pandas
  	* numpy
  	* requests
    * bs4
  	* xlwt
  	* xlsxwriter
  
  
