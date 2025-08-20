# Biomechanical Assessment Radar Chart Generator in R
# Load required libraries
library(ggplot2)
library(dplyr)
library(gridExtra)
library(scales)

# Function to create radar chart data
prepare_radar_data <- function(gold_standard, left_values, right_values, movement_names) {
  # Create data frame
  data <- data.frame(
    Movement = factor(movement_names, levels = movement_names),
    Gold_Standard = gold_standard,
    Left = left_values,
    Right = right_values
  )
  
  # Add angles for polar coordinates
  n_movements <- length(movement_names)
  data$angle <- seq(0, 2*pi, length.out = n_movements + 1)[1:n_movements]
  
  return(data)
}

# Function to convert to polar coordinates for plotting
polar_coords <- function(r, theta) {
  data.frame(
    x = r * cos(theta),
    y = r * sin(theta)
  )
}

# Function to create radar chart
create_radar_chart <- function(gold_standard, left_values, right_values, movement_names, 
                              title = "Biomechanical Assessment Radar Chart", 
                              save_path = NULL) {
  
  # Prepare data
  radar_data <- prepare_radar_data(gold_standard, left_values, right_values, movement_names)
  
  # Find max value for scaling
  max_val <- max(c(left_values, right_values, gold_standard))
  axis_max <- ceiling(max_val / 20) * 20
  
  # Create grid circles
  grid_values <- seq(20, axis_max, by = 20)
  
  # Convert to Cartesian coordinates for plotting
  plot_data <- data.frame()
  
  # Gold Standard
  gold_coords <- polar_coords(radar_data$Gold_Standard, radar_data$angle)
  gold_coords$type <- "Gold Standard"
  gold_coords$Movement <- radar_data$Movement
  
  # Left values
  left_coords <- polar_coords(radar_data$Left, radar_data$angle)
  left_coords$type <- "Left"
  left_coords$Movement <- radar_data$Movement
  
  # Right values
  right_coords <- polar_coords(radar_data$Right, radar_data$angle)
  right_coords$type <- "Right"
  right_coords$Movement <- radar_data$Movement
  
  # Combine all data
  plot_data <- rbind(gold_coords, left_coords, right_coords)
  
  # Close the polygons by adding first point at the end
  for(type_name in unique(plot_data$type)) {
    first_point <- plot_data[plot_data$type == type_name, ][1, ]
    plot_data <- rbind(plot_data, first_point)
  }
  
  # Create grid circles data
  grid_data <- data.frame()
  for(radius in grid_values) {
    angles <- seq(0, 2*pi, length.out = 100)
    circle_coords <- polar_coords(radius, angles)
    circle_coords$radius <- radius
    grid_data <- rbind(grid_data, circle_coords)
  }
  
  # Create grid lines data
  grid_lines <- data.frame()
  for(i in 1:length(movement_names)) {
    angle <- radar_data$angle[i]
    line_coords <- polar_coords(c(0, axis_max), c(angle, angle))
    line_coords$line_id <- i
    grid_lines <- rbind(grid_lines, line_coords)
  }
  
  # Create axis labels positions
  label_distance <- axis_max * 1.15
  label_coords <- polar_coords(rep(label_distance, length(movement_names)), radar_data$angle)
  label_coords$Movement <- movement_names
  
  # Create the plot
  p <- ggplot() +
    # Grid circles
    geom_path(data = grid_data, aes(x = x, y = y, group = radius), 
              color = "#c9ada7", linetype = "dashed", alpha = 0.7, size = 0.5) +
    # Grid lines
    geom_path(data = grid_lines, aes(x = x, y = y, group = line_id), 
              color = "#c9ada7", linetype = "dashed", alpha = 0.7, size = 0.5) +
    # Data polygons with fill
    geom_polygon(data = plot_data, aes(x = x, y = y, fill = type), alpha = 0.3) +
    # Data lines
    geom_path(data = plot_data, aes(x = x, y = y, color = type, group = type), size = 1.5) +
    # Data points
    geom_point(data = plot_data[plot_data$Movement != "", ], 
               aes(x = x, y = y, color = type), size = 3, alpha = 0.9) +
    # Movement labels
    geom_text(data = label_coords, aes(x = x, y = y, label = Movement), 
              hjust = 0.5, vjust = 0.5, size = 4, fontface = "bold", color = "#f2e9e4") +
    # Grid value labels
    geom_text(data = data.frame(x = 0, y = grid_values, label = grid_values),
              aes(x = x, y = y, label = label), hjust = -0.2, vjust = 0.5, 
              size = 3, color = "#c9ada7") +
    # Styling
    scale_color_manual(values = c("Gold Standard" = "#34a853", "Left" = "#4285f4", "Right" = "#ea4335")) +
    scale_fill_manual(values = c("Gold Standard" = "#34a853", "Left" = "#4285f4", "Right" = "#ea4335")) +
    coord_fixed() +
    theme_void() +
    theme(
      plot.background = element_rect(fill = "#22223b", color = NA),
      panel.background = element_rect(fill = "#494a4e", color = NA),
      plot.title = element_text(hjust = 0.5, size = 16, fontface = "bold", color = "#8f847f", margin = margin(b = 20)),
      legend.position = "top",
      legend.title = element_blank(),
      legend.text = element_text(color = "white", size = 12),
      legend.background = element_rect(fill = "transparent", color = NA),
      plot.margin = margin(20, 20, 20, 20)
    ) +
    labs(title = title) +
    xlim(-axis_max * 1.3, axis_max * 1.3) +
    ylim(-axis_max * 1.3, axis_max * 1.3)
  
  # Save or display
  if (!is.null(save_path)) {
    ggsave(save_path, plot = p, width = 8, height = 8, dpi = 300, bg = "#22223b")
    cat("Chart saved to:", save_path, "\n")
  }
  
  return(p)
}

# Generate synthetic biomechanical data
generate_synthetic_data <- function() {
  # Ankle/Foot data
  ankle_movements <- c("Dorsiflexion Range", "Plantarflexion Range", "Dorsiflexion Force", "Plantarflexion Force")
  ankle_gold <- c(20, 50, 30, 45)
  ankle_left <- c(18, 45, 25, 40)
  ankle_right <- c(19, 48, 28, 42)
  
  # Knee data
  knee_movements <- c("Flexion Range", "Extension Range", "Flexion Force", "Extension Force")
  knee_gold <- c(135, 0, 45, 60)
  knee_left <- c(120, 5, 38, 52)
  knee_right <- c(125, 3, 42, 58)
  
  # Hip data
  hip_movements <- c("Flexion Range", "Extension Range", "Abduction Range", "Adduction Range", "Ext Rotation Range", "Int Rotation Range")
  hip_gold <- c(120, 30, 45, 25, 45, 35)
  hip_left <- c(110, 25, 40, 22, 38, 30)
  hip_right <- c(115, 28, 42, 24, 40, 32)
  
  # Shoulder data
  shoulder_movements <- c("Ext Rotation Range", "Int Rotation Range", "Flexion Range", "Extension Range")
  shoulder_gold <- c(90, 70, 180, 60)
  shoulder_left <- c(85, 65, 160, 55)
  shoulder_right <- c(88, 68, 170, 58)
  
  return(list(
    ankle = list(movements = ankle_movements, gold = ankle_gold, left = ankle_left, right = ankle_right),
    knee = list(movements = knee_movements, gold = knee_gold, left = knee_left, right = knee_right),
    hip = list(movements = hip_movements, gold = hip_gold, left = hip_left, right = hip_right),
    shoulder = list(movements = shoulder_movements, gold = shoulder_gold, left = shoulder_left, right = shoulder_right)
  ))
}

# Generate and display synthetic data
cat("Generating synthetic biomechanical assessment data...\n")
synthetic_data <- generate_synthetic_data()

# Print data summary
cat("\n=== SYNTHETIC DATA SUMMARY ===\n")
for(joint_name in names(synthetic_data)) {
  joint_data <- synthetic_data[[joint_name]]
  cat("\n", toupper(joint_name), "ASSESSMENT:\n")
  cat("Movements:", paste(joint_data$movements, collapse = ", "), "\n")
  cat("Gold Standard:", paste(joint_data$gold, collapse = ", "), "\n")
  cat("Left Values:", paste(joint_data$left, collapse = ", "), "\n")
  cat("Right Values:", paste(joint_data$right, collapse = ", "), "\n")
}

# Create charts for each joint
cat("\n=== CREATING RADAR CHARTS ===\n")

# Create output directory if it doesn't exist
if (!dir.exists("charts")) {
  dir.create("charts")
  cat("Created 'charts' directory\n")
}

# Generate charts
for(joint_name in names(synthetic_data)) {
  joint_data <- synthetic_data[[joint_name]]
  
  cat("Creating", joint_name, "radar chart...\n")
  
  chart <- create_radar_chart(
    gold_standard = joint_data$gold,
    left_values = joint_data$left,
    right_values = joint_data$right,
    movement_names = joint_data$movements,
    title = paste(toupper(joint_name), "Assessment"),
    save_path = paste0("charts/", joint_name, "_radar_chart.png")
  )
  
  # Display the chart
  print(chart)
}

# Create summary statistics
cat("\n=== SUMMARY STATISTICS ===\n")
summary_stats <- data.frame()

for(joint_name in names(synthetic_data)) {
  joint_data <- synthetic_data[[joint_name]]
  
  # Calculate percentages relative to gold standard
  left_percentages <- round((joint_data$left / joint_data$gold) * 100, 1)
  right_percentages <- round((joint_data$right / joint_data$gold) * 100, 1)
  
  # Calculate asymmetry
  asymmetry <- round(abs(joint_data$left - joint_data$right) / 
                    ((joint_data$left + joint_data$right) / 2) * 100, 1)
  
  # Create summary for this joint
  joint_summary <- data.frame(
    Joint = rep(toupper(joint_name), length(joint_data$movements)),
    Movement = joint_data$movements,
    Gold_Standard = joint_data$gold,
    Left_Value = joint_data$left,
    Right_Value = joint_data$right,
    Left_Percentage = paste0(left_percentages, "%"),
    Right_Percentage = paste0(right_percentages, "%"),
    Asymmetry = paste0(asymmetry, "%"),
    stringsAsFactors = FALSE
  )
  
  summary_stats <- rbind(summary_stats, joint_summary)
}

# Print summary table
print(summary_stats)

# Save summary to CSV
write.csv(summary_stats, "biomechanical_assessment_summary.csv", row.names = FALSE)
cat("\nSummary statistics saved to 'biomechanical_assessment_summary.csv'\n")

cat("\n=== SCRIPT COMPLETED ===\n")
cat("Generated", length(synthetic_data), "radar charts and saved to 'charts/' directory\n")
cat("All charts use synthetic data that mimics real biomechanical assessment patterns\n")