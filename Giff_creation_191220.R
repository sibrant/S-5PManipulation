## based on tutorial from
###https://ryanpeek.github.io/2016-10-19-animated-gif_maps_in_R/

library(raster)

library(viridis) # nice color palette
library(ggplot2) # plotting
library(ggmap) # ggplot functionality for maps
library(dplyr) # use for fixing up data
library(readr) # reading in data/csv
library(RColorBrewer) # for color palettes
library(purrr) # for mapping over a function
library(magick) # this is call to animate/read pngs
library(jpeg)

library(stringr)

setwd("C:/Users/Administrator/Documents/ClujTrainingCourse_S5P")

tif_dir = 'export_aus/NO2'

tif_lst = list.files(tif_dir, pattern = 'tif$', full.names = T)

dt_st_lst = as.vector(t(as.data.frame(str_extract_all(tif_lst, "[A-Za-z0-9]+"))[7,]))
dt_end_lst = as.vector(t(as.data.frame(str_extract_all(tif_lst, "[A-Za-z0-9]+"))[8,]))



#open one file to get coordinate info for basemap
r = raster(tif_lst[1])
date = dt_st_lst[1]

r = flip(r, 'y')

crs(r) <- "+init=epsg:4326"

r[r < 0] <- NA

plot(r)

# Get the basemap
register_google(key = "AIzaSyAhh2E6PZHtELFIjD1urta9apwca31G7HI", write = TRUE)

bm <- get_map(as.vector(bbox(r)),
  zoom=6,
  crop = T,
  maptype = 'terrain',
  color="color", 
  source = 'stamen')

plot(bm)

gg <- ggmap(bm, extent='panel',padding=0) 

x_min = layer_scales(gg)$x$range$range[1]
y_min = layer_scales(gg)$y$range$range[1]
y_max = layer_scales(gg)$y$range$range[2]
x_max = layer_scales(gg)$x$range$range[2]
x_avg = (x_max+x_min)/2

#open creodias logo
img <- as.raster(readJPEG(source = 'logo.jpg'))
rat = nrow(img)/ncol(img)

#create maps of each date range
for (i in 1:length(tif_lst)) {

  r = raster(tif_lst[i])
  date_st = dt_st_lst[i]
  date_end = dt_end_lst[i]
 
  date_st_nice = paste0(substr(date_st,7,8),'/',substr(date_st,5,6),'/',substr(date_st,1,4))
  date_end_nice = paste0(substr(date_end,7,8),'/',substr(date_end,5,6),'/',substr(date_end,1,4))
  
  r = flip(r, 'y')
  
  crs(r) <- "+init=epsg:4326"
  
  #plot(r)
  
  test_spdf <- as(r, "SpatialPixelsDataFrame")
  test_df <- as.data.frame(test_spdf)
  colnames(test_df) <- c("value", "x", "y")
  
  #for aai
  r[r < 0] <- NA
  fn = 'AAI'
  gg +
    geom_tile(data=test_df, aes(x=x, y=y, fill=value), alpha=0.8) + 
    scale_fill_viridis(option = 'inferno', limits=c(0, 8)) +
    ggtitle('Sentinel-5P L2 Absorbing Aerosol Index') +
    labs(fill = 'Absorbing \nAerosol \nIndex') +

    
  #for so2
  # r[r < 1] <- NA
  # fn = 'SO2'
  # gg +
  #   geom_tile(data=test_df, aes(x=x, y=y, fill=value), alpha=0.8) + 
  #   scale_fill_viridis(option = 'inferno',limits=c(1, 30)) +
  #   ggtitle('Sentinel-5P L2 SO2 Vertical Column Amount') +
  #   labs(fill = 'SO2 Total \nColumn (7km)') +

  #for co
  # r[r < 0.05] <- NA
  # fn = 'CO'
  # gg +
  #   geom_tile(data=test_df, aes(x=x, y=y, fill=value), alpha=0.8) + 
  #   scale_fill_viridis(option = 'inferno',limits=c(0.05, 0.6)) +
  #   ggtitle('Sentinel-5P L2 CO Column Density') +
  #   labs(fill = 'CO Column \nDensity [mol/m^2]') +
  
 
  #for no2
  # fn = 'NO2'
  # r[r < 1] <- NA
  # gg +
  #   geom_tile(data=test_df, aes(x=x, y=y, fill=value), alpha=0.8) +
  #   scale_fill_viridis(option = 'inferno',limits=c(1, 30)) +
  #   ggtitle('Sentinel-5P L2 NO2 Vertical Column Density') +
  #   labs(fill = 'NO2 Column \nDensity [mol/m^2]') +
    
    coord_equal() +

    ylab("Latitude") + xlab("Longitude") +
  
    theme(
      plot.title = element_text(hjust = 0.5, size = 12, face="bold"),
      axis.text.x = element_text(vjust=0.25, size=10),
      axis.text.y = element_text(vjust=0.25, size=10),
          legend.position=c(1,0),legend.justification=c(1,0),
          legend.direction="vertical",legend.text=element_text(size=10),
          legend.title=element_text(size=10),
          legend.box="horizontal", panel.background = element_blank(),
          legend.box.just = c("top"), 
          legend.background = element_rect(fill=alpha('white', 0.6), colour = "gray30")) +
    geom_label(label = paste0(date_st_nice, ' - ', date_end_nice),  x = x_min+0.3, y = y_min+0.3,  size = 5,  vjust = 'bottom', hjust = 'left') +
    annotation_raster(img, xmin=x_min+0.5, xmax=x_min+0.5+4, ymin=y_max-0.5-4*rat, ymax=y_max-0.5) +
    annotate("rect", xmin=x_min+0.5, xmax=x_min+0.5+4, ymin=y_max-0.5-4*rat, ymax=y_max-0.5, fill=NA, colour='black')
    
    # annotation_raster(img, xmin=x_avg-2, xmax=x_avg+2, ymin=y_min+0.3, ymax=y_min+0.3+4*rat) +
    # annotate("rect", xmin=x_avg-2, xmax=x_avg+2, ymin=y_min+0.3, ymax=y_min+0.3+4*rat, fill=NA, colour='black')
  
  ggsave(filename = paste0(tif_dir, '/', fn, '_', date_st, '-', date_end, '.png'),
         width = 7,height=5,dpi = 200)
  
}

#animate maps into GIFF
list.files(tif_dir, pattern = "*.png", full.names = T) %>% 
  map(image_read) %>% # reads each path file
  image_join() %>% # joins image
  image_animate(fps=0.5) %>% # animates, can opt for number of loops
  image_write(paste0(tif_dir, "/AAI_animated.gif")) # write to current dir

