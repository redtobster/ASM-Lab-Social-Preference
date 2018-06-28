library(ggplot2)
library(RColorBrewer)
library(shiny)
library(repr)
library(gridExtra)

################################################################################################
# Generating suitable confidence interval plot

clean_up <- function(df){
  # removing the NA and the sex columns
  if (ncol(df) > 22){
    index <- seq_len(ncol(df))[-(23:ncol(df))]
    df <- df[, index]
  }

  # transposing the dfs
  df <- as.data.frame(t(df))[-c(1,2),]
}

# function to make sure the different types have equal number of rows
make_equal <- function(lst){
  l1 <- nrow(lst[[1]])
  l2 <- nrow(lst[[7]])
  ifelse(l1 < l2, lst <- lapply(lst, head, n = nrow(lst[[1]])),
         ifelse(l1 > l2, lst <- lapply(lst, head, n = nrow(lst[[7]])),
                lst))
  return(lst)
}

# function that takes the analyzed list and organize it to be ready for plotting
get_list <- function(lst, type1, type2){
  if (length(lst) == 12){
    # getting the mean, upper and lower values for plotting later
    lst <- lapply(lst, tail, n = 4)
    lst <- lapply(lst, clean_up)
    lst <- make_equal(lst)
    
    # creating the x-axis labels
    time2 <- seq_len(nrow(lst[[1]]))
    time1 <- seq_len(nrow(lst[[1]])) - 1
    time <- paste(time1, time2, sep = "-")
    
    # creating proper colnames
    colnames <- c("mean", "lower", "upper", "time", "Type")
    
    # assigning the type of fish, the x-axis labels, col and row names of dfs
    for (i in seq_len(length(lst))){
      # assigning the x-axis labels
      lst[[i]][, 4] <- factor(time, levels = time)
      # assigning the type of the fish
      ifelse(i < 7, lst[[i]][,5] <- type1, lst[[i]][,5] <- type2)
      # assigning the colnames and rownames
      colnames(lst[[i]]) <- colnames
      rownames(lst[[i]]) <- NULL
    }
    
    # data conversion before plotting from factors to integers
    for (i in seq_len(length(lst))) {
      for(j in seq_len(3)){
        lst[[i]][,j] <- as.numeric(as.character(lst[[i]][,j]))
      }
    }
    
    # combining the two types of dfs
    for (i in seq_len(length(lst)/2)){
      lst[[i]] <- rbind(lst[[i]], lst[[i+(length(lst)/2)]])
    }
    return(lst[1:6])
  } else {
    return(lst)
  }
}

# function that takes in a df
plot_CI <- function(df, string){
  annotations <- data.frame(
    xpos = -Inf,
    ypos =  Inf,
    annotateText = string,
    hjustvar = 0,
    vjustvar = 1)

  color <- brewer.pal(3, "Set2")[c(1,2)]
  ggplot(df, aes(time, mean, group = Type)) +
    geom_point(aes(color = Type)) +
    coord_cartesian(ylim = c(0, 100)) +
    geom_line(aes(color = Type)) +
    geom_ribbon(aes(fill = Type, ymin = lower, ymax = upper), alpha = 0.3, colour=NA) +
    theme(legend.position = "none") +
    scale_fill_manual(values = color) +
    scale_color_manual(values = color) +
    labs(x = "Time (minute interval)",
         y = "Percentage") +
    theme_classic() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0, margin = margin(r = 0))) +
    theme(legend.position = c(0.89, 0.85)) +
    theme(text = element_text(family="Helvetica")) +
    geom_text(data = annotations, aes(x=xpos,y=ypos,hjust=hjustvar,vjust=vjustvar,label=annotateText,group=1))
    
}

##########################################################################################################
# Generating suitable list for scatter plot by sex

# some general clean-ups (removing NA values and the sex columns) and transposing the dfs
clean_up_sex <- function(df){
  # removing the NA columns
  if (ncol(df) > 22){
    index_to_delete <- seq(23, ncol(df)) # limit to 20 minutes only
    df <- df[, -index_to_delete]
  }
  
  # removing the rows with NAs at the last columns
  row_delete <- which(is.na(df[,ncol(df)]))
  if (length(row_delete > 1)){
    df <- df[-row_delete,]  
  }
  
  # transposing the dfs
  df <- as.data.frame(t(df))[-1,]
  col_df <- ncol(df)
  df <- df[, -((col_df-3):col_df)]
  number_of_minutes <- nrow(df)
  df <- as.data.frame(unlist(df))
  
  # unfactorizing the df
  df <- data.frame(lapply(df, as.character), stringsAsFactors=FALSE)
  
  # populating second column with the sex of the fish
  for (i in seq_len(nrow(df))){
    if ((i-1) %% number_of_minutes == 0){
      sex <- tolower(df[i,1])
      df[i,2] <- sex
    } else {
      df[i,2] <- sex
    }
  }
  
  # deleting the rows with no numbers at all
  df <- df[-grep(".*ale", df[,1]),]
  number_of_files <- nrow(df)/(number_of_minutes-1)
  
  # creating the x-axis labels
  time2 <- seq_len(number_of_minutes-1)
  time1 <- seq_len(number_of_minutes-1) - 1
  time <- rep(paste(time1, time2, sep = "-"), times = number_of_files)
  df[,3] <- time
  
  return(df)
}


# function to make sure the different types have equal number of rows
make_equal_time <- function(lst){
  t1 <- as.numeric(sub("([0-9]*)-.*", "\\1", tail(lst[[1]], n = 1)[3]))
  number_of_files_1 <- nrow(lst[[1]])/(t1+1)
  number_of_minutes_1 <- t1 + 1
  t2 <- as.numeric(sub("([0-9]*)-.*", "\\1", tail(lst[[7]], n = 1)[3]))
  number_of_files_2 <- nrow(lst[[7]])/(t2+1)
  number_of_minutes_2 <- t2 + 1
  if (t1 > t2){
    first_index <- (((t1+1)-(t1-t2))+1):(t1+1)
    single_index <- seq(from = 0, to = nrow(lst[[1]])-number_of_minutes_1, 
                        by = number_of_minutes_1)
    pre_index <- rep(single_index, each = t1-t2)
    index_to_delete <- pre_index + first_index
    for (i in seq_len(length(lst)/2)){
      lst[[i]] <- lst[[i]][-index_to_delete, ]
    }
  } else if (t1 < t2) {
    first_index <- (((t2+1)-(t2-t1))+1):(t2+1)
    single_index <- seq(from = 0, to = nrow(lst[[7]])-number_of_minutes_2, 
                        by = number_of_minutes_2)
    pre_index <- rep(single_index, each = t2-t1)
    index_to_delete <- pre_index + first_index
    for (i in seq(from = (length(lst)/2)+1, to = length(lst))){
      lst[[i]] <- lst[[i]][-index_to_delete, ]
    }
  } else {
    lst <- lst
  }
  return(lst)
}

# function that takes the mean list and then makes sure that each type 
# has equal number of rows.
make_equal_mean <- function(lst){
  l1 <- nrow(lst[[1]])
  l2 <- nrow(lst[[7]])
  ifelse(l1 < l2, lst <- lapply(lst, head, n = nrow(lst[[1]])),
         ifelse(l1 > l2, lst <- lapply(lst, head, n = nrow(lst[[7]])),
                lst))
  return(lst)
}

# function that takes the analyzed list and organize it to be ready for plotting
get_list_sex <- function(lst, type1, type2){
  if (length(lst) == 12){
    # getting the mean only
    mean_lst <- lapply(lapply(lst, tail, n = 4), head, n = 1)
    mean_lst <- lapply(mean_lst, function(x) x[,-c(1,2)])
    mean_lst <- lapply(mean_lst, t)
    mean_lst <- make_equal_mean(mean_lst)
    number_of_minutes <- nrow(mean_lst[[1]])
    
    # creating the x-axis labels
    time2 <- seq_len(number_of_minutes)
    time1 <- seq_len(number_of_minutes) - 1
    time <- paste(time1, time2, sep = "-")
    
    for (i in seq_len(length(mean_lst))){
      values <- as.numeric(mean_lst[[i]][,1])
      mean_lst[[i]] <- as.data.frame(mean_lst[[i]], time, values)
      mean_lst[[i]][,2] <- factor(time, levels = time)
    }
    
    # processing the list
    lst <- lapply(lst, clean_up_sex)
    lst <- make_equal_time(lst)
    
    # creating proper colnames
    colnames <- c("percent", "Sex", "time", "Type")
    colnames_mean <- c("percent", "time", "Type")
    
    # assigning the type of fish, the x-axis labels, col and row names of dfs
    for (i in seq_len(length(lst))){
      # assigning the type of the fish
      ifelse(i < 7, lst[[i]][,4] <- type1, lst[[i]][,4] <- type2)
      ifelse(i < 7, mean_lst[[i]][,3] <- type1, mean_lst[[i]][,3] <- type2)
      # assigning the colnames and rownames
      colnames(lst[[i]]) <- colnames
      rownames(lst[[i]]) <- NULL
      colnames(mean_lst[[i]]) <- colnames_mean
      rownames(mean_lst[[i]]) <- NULL
    }
    
    # data conversion before plotting from factors to integers
    for (i in seq_len(length(lst))) {
      lst[[i]][,1] <- as.numeric(lst[[i]][,1])
    }
    
    for (i in seq_len(length(mean_lst))){
      lst[[i]] <- list(lst[[i]], mean_lst[[i]])
    }
    
    
    # naming the list appropriately to ensure that mean is distinct
    w <- list("df_quad4.csv", "zdf_quad4.csv",
              "df_half1.csv", "zdf_half1.csv",
              "df_half2.csv", "zdf_half2.csv",
              "df_quad1.csv", "zdf_quad1.csv",
              "df_quad2.csv", "zdf_quad2.csv",
              "df_quad3.csv", "zdf_quad3.csv")
    w <- sort(unlist(w))
    
    names(lst) <- w
    
    return(lst)
  } else {
    return(lst)
  }
}

# function to get the index of the subset based on the desired minute interval
subset_sex_df <- function(df, n){
  row_number <- nrow(df)
  max_minute <- as.numeric(sub("[0-9]*-","",df[row_number, 3]))
  if (n >= max_minute){
    index_to_subset <- seq(from = 1, to = row_number)
  } else {
    file_number <- row_number/max_minute
    to_delete_seq <- (n+1):max_minute
    pre_to_delete_index <- rep(seq(from = 0, to = row_number-max_minute,
                                   by = max_minute), each = max_minute-n)
    index_to_delete <- pre_to_delete_index + to_delete_seq
    index_to_subset <- seq(from = 1, to = row_number)[-index_to_delete]
  }
  return(index_to_subset)
}

# plotting function for the scatterplot by sex
plot_sex <- function(df1, df2){
  annotations <- data.frame(
    xpos = Inf,
    ypos =  Inf,
    annotateText = paste("Fish Type:", df2[1,3]),
    hjustvar = 1,
    vjustvar = 1) #<- adjust
  
  color <- brewer.pal(3, "Set3")[1]
  color_sex <- brewer.pal(3, "Set2")[c(2,3)]
  ggplot(df2, aes(time, percent, group = 1)) +
    geom_line(stat = 'identity', color = color, size = 2) +
    coord_cartesian(ylim = c(0, 100)) +
    geom_point(data = df1, aes(colour = Sex), alpha = 0.5) +
    scale_color_manual(values = color_sex) +
    labs(x = "Time (minute interval)",
         y = "Percentage") +
    geom_text(data = annotations, aes(x=xpos,y=ypos,hjust=hjustvar,vjust=vjustvar,label=annotateText)) +
    theme_classic() +
    theme(axis.text.x = element_text(angle = 90, hjust = 1, vjust = 0, margin = margin(r = 0)))
}

# function to get the legend of the plot
# this is used for the grid extra package
g_legend<-function(a.gplot){
  tmp <- ggplot_gtable(ggplot_build(a.gplot))
  leg <- which(sapply(tmp$grobs, function(x) x$name) == "guide-box")
  legend <- tmp$grobs[[leg]]
  return(legend)}

#################################################################################################
# Code for the ui and the server of the app


ui <- fluidPage(
  titlePanel(
    "ASM Lab Zebra Fish Social Preference Visualization Tool"
  ),
  sidebarLayout(
    # Sidebar with that allows multiple files to be uploaded
    sidebarPanel(helpText("Create plots based on analyzed data of the social behaviour
                          experiment. Please input the types of fish used and subsequently,
                          all 6 csv files from the folder extracted_info_xx."),
                 textInput("text1", "Fish Type 1",
                           value = "Wild Type"),
                 textInput("text2", "Fish Type 2",
                           value = "ILR"),
                 actionButton("go", label = "Confirm"),
                 uiOutput("uioutput1"),
                 uiOutput("uioutput2")),
    mainPanel(verbatimTextOutput("text"),
              plotOutput("plot1"),
              uiOutput('downloadUI'),
              plotOutput("plot2"),
              plotOutput("plot3"),
              plotOutput("plot4"),
              plotOutput("plot5"),
              plotOutput("plot6")
    )
    )
)


server <- function(input, output, session) {
  
  observeEvent(input$go, output$uioutput1 <- renderUI({ div(fileInput("dynamic1", label = h4(paste0("Extracted CSV File (", isolate(input$text1), ")")), 
                                                                      multiple = TRUE, accept = c('text/csv',
                                                                                                  'text/comma-separated-values',
                                                                                                  '.csv')),
                                                            fileInput("dynamic2", label = h4(paste0("Extracted CSV File (", isolate(input$text2), ")")), 
                                                                      multiple = TRUE, accept = c('text/csv',
                                                                                                  'text/comma-separated-values',
                                                                                                  '.csv')),
                                                            actionButton("dynamic3", label = "Validate My CSV Files"))
  })
  )
  # "msg" is a list of objects that can change interactively when
  # the user changes the input.
  msg <- reactiveValues(txt = "")
  # variables to control the sequence of processes 
  controlVar <- reactiveValues(fileReady = FALSE)
  controlVarPlot <- reactiveValues(plotReady = FALSE)
  controlVarPlotSex <- reactiveValues(plotReadySex = FALSE)
  
  # handle the file reading
  observeEvent(c(input$dynamic1, input$dynamic2), msg$txt <- "")
  
  # preparing the list of dfs before the button is clicked
  list_variable <- reactiveValues(lst = list())
  
  # show buttons only when file is uploaded
  observeEvent(input$dynamic3, 
               {
                 controlVar$fileReady <- FALSE
                 if (is.null(input$dynamic1) || is.null(input$dynamic2)){
                   msg$txt <- "ERROR: Please complete uploading the CSV files."
                   return(NULL)
                 }
                 lst1 <- list()
                 lstname1 <- list()
                 for(i in seq_len(length(input$dynamic1[,1]))){
                   lst1[[i]] <- read.csv(input$dynamic1[[i, 'datapath']])
                   lstname1[[i]] <- input$dynamic1[[i, 'name']]
                 }
                 lst2 <- list()
                 lstname2 <- list()
                 for(i in seq_len(length(input$dynamic2[,1]))){
                   lst2[[i]] <- read.csv(input$dynamic2[[i, 'datapath']])
                   lstname2[[i]] <- paste0("z",input$dynamic2[[i, 'name']])
                 }
                 list_variable$lst <- c(lst1, lst2)
                 lstname <- c(lstname1, lstname2)
                 names(list_variable$lst) <- lstname
                 lstname <- sort(unlist(lstname))
                 list_variable$lst <- list_variable$lst[lstname]
                 if((length(list_variable$lst) == 12) && all(sapply(list_variable$lst, is.data.frame))){
                   controlVar$fileReady <- TRUE
                   msg$txt <- "Ready to Plot"
                   return(list_variable$lst)
                 } else {
                   msg$txt <- "ERROR: Please upload 6 CSV files only per fish type"
                   return(NULL)
                 }
               })
  output$text <- renderPrint(cat(msg$txt))
  output$uioutput2 <- renderUI({
    if (controlVar$fileReady){
      box_name <- vector()
      for (i in seq_len(12)){
        ifelse(i < 5, box_name[i] <- paste("Quadrant", i, input$text1), 
               ifelse(i < 7, box_name[i] <- paste("Half", i-4, input$text1), 
                      ifelse(i < 11, box_name[i] <- paste("Quadrant", i-6, input$text2), 
                             box_name[i] <- paste("Half", i-10, input$text2))))
      }
      div(checkboxInput("box1", box_name[1], value = T),
          checkboxInput("box2", box_name[2], value = F),
          checkboxInput("box3", box_name[3], value = F),
          checkboxInput("box4", box_name[4], value = F),
          checkboxInput("box5", box_name[5], value = F),
          checkboxInput("box6", box_name[6], value = F),
          checkboxInput("box7", box_name[7], value = T ),
          checkboxInput("box8", box_name[8], value = F),
          checkboxInput("box9", box_name[9], value = F),
          checkboxInput("box10", box_name[10], value = F),
          checkboxInput("box11", box_name[11], value = F),
          checkboxInput("box12", box_name[12], value = F),
          sliderInput("freq", "Minute intervals:",
                      min = 1, max = 20, value = 10),
          actionButton('sexbutton','Render Scatterplot by Sex'),
          actionButton('cibutton','Render CI Plot'),
          downloadButton('downloadPlot', 'Download Plots as PDF')
      ) 
    }
  })
  
  plot_test <- eventReactive(input$cibutton, {
    lst1 <- list()
    lstname1 <- list()
    for(i in seq_len(length(input$dynamic1[,1]))){
      lst1[[i]] <- read.csv(input$dynamic1[[i, 'datapath']])
      lstname1[[i]] <- input$dynamic1[[i, 'name']]
    }
    lst2 <- list()
    lstname2 <- list()
    for(i in seq_len(length(input$dynamic2[,1]))){
      lst2[[i]] <- read.csv(input$dynamic2[[i, 'datapath']])
      lstname2[[i]] <- paste0("z",input$dynamic2[[i, 'name']])
    }
    list_variable$lst <- c(lst1, lst2)
    lstname <- c(lstname1, lstname2)
    names(list_variable$lst) <- lstname
    lstname <- sort(unlist(lstname))
    list_variable$lst <- list_variable$lst[lstname]
    list_variable$lst <- get_list(list_variable$lst, input$text1, input$text2)
  })
  
  plot_test_sex <- eventReactive(input$sexbutton, {
    lst1 <- list()
    lstname1 <- list()
    for(i in seq_len(length(input$dynamic1[,1]))){
      lst1[[i]] <- read.csv(input$dynamic1[[i, 'datapath']])
      lstname1[[i]] <- input$dynamic1[[i, 'name']]
    }
    lst2 <- list()
    lstname2 <- list()
    for(i in seq_len(length(input$dynamic2[,1]))){
      lst2[[i]] <- read.csv(input$dynamic2[[i, 'datapath']])
      lstname2[[i]] <- paste0("z",input$dynamic2[[i, 'name']])
    }
    list_variable$lst <- c(lst1, lst2)
    lstname <- c(lstname1, lstname2)
    names(list_variable$lst) <- lstname
    lstname <- sort(unlist(lstname))
    list_variable$lst <- list_variable$lst[lstname]
    list_variable$lst <- get_list_sex(list_variable$lst, input$text1, input$text2)
  })
  
  observeEvent(input$cibutton, {
    controlVarPlotSex$plotReadySex <- FALSE
    controlVarPlot$plotReady <- TRUE
  })
  
  observeEvent(input$sexbutton, {
    controlVarPlot$plotReady <- FALSE
    controlVarPlotSex$plotReadySex <- TRUE
  })
  
  
  plotInput <- reactive({
    if (controlVarPlot$plotReady == TRUE){
      if(!(input$box7) && !(input$box1)){
        p1 <- NULL
      } else if (!(input$box7)) {
        p1 <- plot_CI(plot_test()[["df_quad1.csv"]][seq_len(input$freq),], paste("Quadrant 1:", input$text1))
      } else if (!(input$box1)) {
        p1 <- plot_CI(plot_test()[["df_quad1.csv"]][seq_len(input$freq) + 
                                                      (nrow(plot_test()[["df_quad1.csv"]])/2),], paste("Quadrant 1:", input$text2))
      } else if ((input$box1) && (input$box7)){
        p1 <- plot_CI(plot_test()[["df_quad1.csv"]][c(seq_len(input$freq), seq_len(input$freq)+
                                                        (nrow(plot_test()[["df_quad1.csv"]])/2)),], paste("Quadrant 1:", input$text1, "v", input$text2))
      }
    } else if (controlVarPlotSex$plotReadySex == TRUE){
      if(!(input$box7) && !(input$box1)){
        p1 <- NULL
      } else if (!(input$box7)) {
        p1 <- plot_sex(plot_test_sex()[["df_quad1.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_quad1.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["df_quad1.csv"]][[2]][seq_len(input$freq),])
      } else if (!(input$box1)) {
        p1 <- plot_sex(plot_test_sex()[["zdf_quad1.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_quad1.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["zdf_quad1.csv"]][[2]][seq_len(input$freq),])
      } else if ((input$box1) && (input$box7)){
        p1a <- plot_sex(plot_test_sex()[["df_quad1.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_quad1.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["df_quad1.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        p1b <- plot_sex(plot_test_sex()[["zdf_quad1.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_quad1.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["zdf_quad1.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        mylegend<-g_legend(p1a)
        p1 <- grid.arrange(arrangeGrob(p1a + theme(legend.position="none"),
                                       p1b + theme(legend.position="none"),
                                       nrow=1),
                           mylegend, nrow=2,heights=c(10, 0.5))
      }
    } else {
      NULL
    }
  })
  
  plotInput2 <- reactive({
    if (controlVarPlot$plotReady == TRUE){
      if(!(input$box8) && !(input$box2)){
        p2 <- NULL
      } else if (!(input$box8)) {
        p2 <- plot_CI(plot_test()[["df_quad2.csv"]][seq_len(input$freq),], paste("Quadrant 2:", input$text1))
      } else if (!(input$box2)) {
        p2 <- plot_CI(plot_test()[["df_quad2.csv"]][seq_len(input$freq) + 
                                                      (nrow(plot_test()[["df_quad2.csv"]])/2),], paste("Quadrant 2:", input$text2))
      } else if ((input$box2) && (input$box8)){
        p2 <- plot_CI(plot_test()[["df_quad2.csv"]][c(seq_len(input$freq), seq_len(input$freq)+
                                                        (nrow(plot_test()[["df_quad2.csv"]])/2)),], paste("Quadrant 2:", input$text1, "v", input$text2))
      }
    } else if (controlVarPlotSex$plotReadySex == TRUE) {
      if(!(input$box8) && !(input$box2)){
        p2 <- NULL
      } else if (!(input$box8)) {
        p2 <- plot_sex(plot_test_sex()[["df_quad2.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_quad2.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["df_quad2.csv"]][[2]][seq_len(input$freq),])
      } else if (!(input$box2)) {
        p2 <- plot_sex(plot_test_sex()[["zdf_quad2.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_quad2.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["zdf_quad2.csv"]][[2]][seq_len(input$freq),])
      } else if ((input$box2) && (input$box8)){
        p2a <- plot_sex(plot_test_sex()[["df_quad2.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_quad2.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["df_quad2.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        p2b <- plot_sex(plot_test_sex()[["zdf_quad2.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_quad2.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["zdf_quad2.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        mylegend<-g_legend(p2a)
        p2 <- grid.arrange(arrangeGrob(p2a + theme(legend.position="none"),
                                       p2b + theme(legend.position="none"),
                                       nrow=1),
                           mylegend, nrow=2,heights=c(10, 0.5))
      }
    } else {
      NULL
    }
  })
  
  plotInput3 <- reactive({
    if (controlVarPlot$plotReady == TRUE){
      if(!(input$box9) && !(input$box3)){
        p3 <- NULL
      } else if (!(input$box9)) {
        p3 <- plot_CI(plot_test()[["df_quad3.csv"]][seq_len(input$freq),], paste("Quadrant 3:", input$text1))
      } else if (!(input$box3)) {
        p3 <- plot_CI(plot_test()[["df_quad3.csv"]][seq_len(input$freq) + 
                                                      (nrow(plot_test()[["df_quad3.csv"]])/2),], paste("Quadrant 3:", input$text2))
      } else if ((input$box3) && (input$box9)){
        p3 <- plot_CI(plot_test()[["df_quad3.csv"]][c(seq_len(input$freq), seq_len(input$freq)+
                                                        (nrow(plot_test()[["df_quad3.csv"]])/2)),], paste("Quadrant 3:", input$text1, "v", input$text2))
      }
    } else if (controlVarPlotSex$plotReadySex == TRUE) {
      if(!(input$box9) && !(input$box3)){
        p3 <- NULL
      } else if (!(input$box9)) {
        p3 <- plot_sex(plot_test_sex()[["df_quad3.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_quad3.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["df_quad3.csv"]][[2]][seq_len(input$freq),])
      } else if (!(input$box3)) {
        p3 <- plot_sex(plot_test_sex()[["zdf_quad3.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_quad3.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["zdf_quad3.csv"]][[2]][seq_len(input$freq),])
      } else if ((input$box3) && (input$box9)){
        p3a <- plot_sex(plot_test_sex()[["df_quad3.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_quad3.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["df_quad3.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        p3b <- plot_sex(plot_test_sex()[["zdf_quad3.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_quad3.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["zdf_quad3.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        mylegend<-g_legend(p3a)
        p3 <- grid.arrange(arrangeGrob(p3a + theme(legend.position="none"),
                                       p3b + theme(legend.position="none"),
                                       nrow=1),
                           mylegend, nrow=2,heights=c(10, 0.5))
      }
    } else {
      NULL
    }
  })
  
  plotInput4 <- reactive({
    if (controlVarPlot$plotReady == TRUE){
      if(!(input$box4) && !(input$box10)){
        NULL
      } else if (!(input$box10)) {
        plot_CI(plot_test()[["df_quad4.csv"]][seq_len(input$freq),], paste("Quadrant 4:", input$text1))  
      } else if (!(input$box4)) {
        plot_CI(plot_test()[["df_quad4.csv"]][seq_len(input$freq) + 
                                                (nrow(plot_test()[["df_quad4.csv"]])/2),], paste("Quadrant 4:", input$text2)) 
      } else if ((input$box4) && (input$box10)){
        plot_CI(plot_test()[["df_quad4.csv"]][c(seq_len(input$freq), seq_len(input$freq)+
                                                  (nrow(plot_test()[["df_quad4.csv"]])/2)),], paste("Quadrant 4:", input$text1, "v", input$text2))
      }
    } else if (controlVarPlotSex$plotReadySex == TRUE) {
      if(!(input$box10) && !(input$box4)){
        p4 <- NULL
      } else if (!(input$box10)) {
        p4 <- plot_sex(plot_test_sex()[["df_quad4.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_quad4.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["df_quad4.csv"]][[2]][seq_len(input$freq),])
      } else if (!(input$box4)) {
        p4 <- plot_sex(plot_test_sex()[["zdf_quad4.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_quad4.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["zdf_quad4.csv"]][[2]][seq_len(input$freq),])
      } else if ((input$box4) && (input$box10)){
        p4a <- plot_sex(plot_test_sex()[["df_quad4.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_quad4.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["df_quad4.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        p4b <- plot_sex(plot_test_sex()[["zdf_quad4.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_quad4.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["zdf_quad4.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        mylegend<-g_legend(p4a)
        p4 <- grid.arrange(arrangeGrob(p4a + theme(legend.position="none"),
                                       p4b + theme(legend.position="none"),
                                       nrow=1),
                           mylegend, nrow=2,heights=c(10, 0.5))
      }
    } else {
      NULL
    }
  })
  
  plotInput5 <- reactive({
    if (controlVarPlot$plotReady == TRUE){
      if(!(input$box5) && !(input$box11)){
        NULL
      } else if (!(input$box11)) {
        plot_CI(plot_test()[["df_half1.csv"]][seq_len(input$freq),], paste("Half 1:", input$text1))  
      } else if (!(input$box5)) {
        plot_CI(plot_test()[["df_half1.csv"]][seq_len(input$freq) + 
                                                (nrow(plot_test()[["df_half1.csv"]])/2),], paste("Half 1:", input$text2)) 
      } else if ((input$box5) && (input$box11)){
        plot_CI(plot_test()[["df_half1.csv"]][c(seq_len(input$freq), seq_len(input$freq)+
                                                  (nrow(plot_test()[["df_half1.csv"]])/2)),], paste("Half 1:", input$text1, "v", input$text2))
      }
    } else if (controlVarPlotSex$plotReadySex == TRUE) {
      if(!(input$box11) && !(input$box5)){
        p5 <- NULL
      } else if (!(input$box11)) {
        p5 <- plot_sex(plot_test_sex()[["df_half1.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_half1.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["df_half1.csv"]][[2]][seq_len(input$freq),])
      } else if (!(input$box5)) {
        p5 <- plot_sex(plot_test_sex()[["zdf_half1.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_half1.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["zdf_half1.csv"]][[2]][seq_len(input$freq),])
      } else if ((input$box5) && (input$box11)){
        p5a <- plot_sex(plot_test_sex()[["df_half1.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_half1.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["df_half1.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        p5b <- plot_sex(plot_test_sex()[["zdf_half1.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_half1.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["zdf_half1.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        mylegend<-g_legend(p5a)
        p5 <- grid.arrange(arrangeGrob(p5a + theme(legend.position="none"),
                                       p5b + theme(legend.position="none"),
                                       nrow=1),
                           mylegend, nrow=2,heights=c(10, 0.5))
      }
    } else {
      NULL
    }
  })
  
  plotInput6 <- reactive({
    if (controlVarPlot$plotReady == TRUE){
      NULL
      if(!(input$box6) && !(input$box12)){
        NULL
      } else if (!(input$box12)) {
        plot_CI(plot_test()[["df_half2.csv"]][seq_len(input$freq),], paste("Half 2:", input$text1))  
      } else if (!(input$box6)) {
        plot_CI(plot_test()[["df_half2.csv"]][seq_len(input$freq) + 
                                                (nrow(plot_test()[["df_half2.csv"]])/2),], paste("Half 2:", input$text2)) 
      } else if ((input$box6) && (input$box12)){
        plot_CI(plot_test()[["df_half2.csv"]][c(seq_len(input$freq), seq_len(input$freq)+
                                                  (nrow(plot_test()[["df_half2.csv"]])/2)),], paste("Half 2:", input$text1, "v", input$text2))
      }
    } else if (controlVarPlotSex$plotReadySex == TRUE) {
      if(!(input$box12) && !(input$box6)){
        p6 <- NULL
      } else if (!(input$box12)) {
        p6 <- plot_sex(plot_test_sex()[["df_half2.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_half2.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["df_half2.csv"]][[2]][seq_len(input$freq),])
      } else if (!(input$box6)) {
        p6 <- plot_sex(plot_test_sex()[["zdf_half2.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_half2.csv"]][[1]], input$freq),], 
                       plot_test_sex()[["zdf_half2.csv"]][[2]][seq_len(input$freq),])
      } else if ((input$box6) && (input$box12)){
        p6a <- plot_sex(plot_test_sex()[["df_half2.csv"]][[1]][subset_sex_df(plot_test_sex()[["df_half2.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["df_half2.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        p6b <- plot_sex(plot_test_sex()[["zdf_half2.csv"]][[1]][subset_sex_df(plot_test_sex()[["zdf_half2.csv"]][[1]], input$freq),], 
                        plot_test_sex()[["zdf_half2.csv"]][[2]][seq_len(input$freq),]) + theme(legend.position="bottom")
        mylegend<-g_legend(p6a)
        p6 <- grid.arrange(arrangeGrob(p6a + theme(legend.position="none"),
                                       p6b + theme(legend.position="none"),
                                       nrow=1),
                           mylegend, nrow=2,heights=c(10, 0.5))
      }
    } else {
      NULL
    }
  })
  
  output$plot1 <- renderPlot({
    if (controlVarPlot$plotReady == FALSE && controlVarPlotSex$plotReadySex == FALSE){
      NULL
    } else {
      print(plotInput())
    }
  })
  output$plot2 <- renderPlot({
    if (controlVarPlot$plotReady == FALSE && controlVarPlotSex$plotReadySex == FALSE){
      NULL
    } else {
      print(plotInput2())
    }
  })
  output$plot3 <- renderPlot({
    if (controlVarPlot$plotReady == FALSE && controlVarPlotSex$plotReadySex == FALSE){
      NULL
    } else {
      print(plotInput3())
    }
  })
  output$plot4 <- renderPlot({
    if (controlVarPlot$plotReady == FALSE && controlVarPlotSex$plotReadySex == FALSE){
      NULL
    } else {
      print(plotInput4())
    }
  })
  output$plot5 <- renderPlot({
    if (controlVarPlot$plotReady == FALSE && controlVarPlotSex$plotReadySex == FALSE){
      NULL
    } else {
      print(plotInput5())
    }
  })
  output$plot6 <- renderPlot({
    if (controlVarPlot$plotReady == FALSE && controlVarPlotSex$plotReadySex == FALSE){
      NULL
    } else {
      print(plotInput6())
    }
  })
  
  output$downloadPlot <- downloadHandler(
    filename = function() { 'Rplots.pdf' },
    content = function(file) {
      pdf(file)
      print( plotInput() )
      print( plotInput2() )
      print( plotInput3() )
      print( plotInput4() )
      print( plotInput5() )
      print( plotInput6() )
      dev.off()
    }
  )
}

shinyApp(ui, server)
