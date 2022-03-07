#!/usr/local/bin/Rscript

library(knitr)
library(rmarkdown)
Sys.setenv(RSTUDIO_PANDOC="/Applications/RStudio.app/Contents/MacOS/pandoc")

base_markdown_name = 'statistical_rethinking.Rmd'

args = commandArgs(trailingOnly=TRUE)
if(length(args) == 0){
	  output_name=gsub('.Rmd$','.pdf',base_markdown_name) 
	  render( base_markdown_name,  output_format="bookdown::pdf_document2", output_dir="output", output_file=output_name                            )
}else{
	for( arg in args ){
	  output_name=gsub('.Rmd$','.pdf',arg) 
	  render( base_markdown_name,  output_format="bookdown::pdf_document2", output_dir="output", output_file=output_name, params=list(chapters=arg) )
	}
}
