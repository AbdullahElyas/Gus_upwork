import numpy as np
import matplotlib.pyplot as plt

def polar_to_xy(r, theta):
    return np.array([r*np.cos(theta), r*np.sin(theta)])

def circle_from_3pts(A, B, C, eps=1e-9):
    x1,y1 = A; x2,y2 = B; x3,y3 = C
    D = 2*(x1*(y2-y3) + x2*(y3-y1) + x3*(y1-y2))
    if abs(D) < eps:
        return None, None
    ux = ((x1**2+y1**2)*(y2-y3) + (x2**2+y2**2)*(y3-y1) + (x3**2+y3**2)*(y1-y2)) / D
    uy = ((x1**2+y1**2)*(x3-x2) + (x2**2+y2**2)*(x1-x3) + (x3**2+y3**2)*(x2-x1)) / D
    O = np.array([ux, uy])
    R = np.hypot(x1-ux, y1-uy)
    return O, R

def angle_ccw(a1, a2):
    d = (a2 - a1) % (2*np.pi)
    return d

def sample_arc(A, B, C, n=50):
    O, R = circle_from_3pts(A, B, C)
    if O is None:
        xs = np.linspace(A[0], C[0], n)
        ys = np.linspace(A[1], C[1], n)
        return np.vstack([xs, ys]).T
    thA = np.arctan2(A[1]-O[1], A[0]-O[0])
    thB = np.arctan2(B[1]-O[1], B[0]-O[0])
    thC = np.arctan2(C[1]-O[1], C[0]-O[0])
    dAC = angle_ccw(thA, thC)
    dAB = angle_ccw(thA, thB)
    if dAB <= dAC:
        ts = np.linspace(thA, thA+dAC, n)
    else:
        dAC_cw = dAC - 2*np.pi
        ts = np.linspace(thA, thA+dAC_cw, n)
    xs = O[0] + R*np.cos(ts)
    ys = O[1] + R*np.sin(ts)
    return np.vstack([xs, ys]).T

def arc_curve(angles, data, points_per_seg=60, bulge=0.0):
    ang = np.array(angles[:-1])
    rad = np.array(data[:-1])
    arc_pts_xy = []
    n = len(ang)
    for i in range(n):
        j = (i+1)%n
        A = polar_to_xy(rad[i], ang[i])
        C = polar_to_xy(rad[j], ang[j])

        M_line = (A + C)/2.0
        chord = C - A
        L = np.linalg.norm(chord)

        if L < 1e-9:
            M = M_line
        else:
            perp = np.array([-chord[1], chord[0]])
            perp /= np.linalg.norm(perp)
            if np.dot(perp, M_line) < 0:
                perp = -perp
            M = M_line + bulge * L * perp

        seg = sample_arc(A, M, C, n=points_per_seg)
        if i>0: seg = seg[1:]
        arc_pts_xy.append(seg)

    arc_pts_xy = np.vstack(arc_pts_xy)
    thetas = np.arctan2(arc_pts_xy[:,1], arc_pts_xy[:,0]) % (2*np.pi)
    rs = np.hypot(arc_pts_xy[:,0], arc_pts_xy[:,1])

    thetas = np.concatenate([thetas, [ang[0]]])
    rs = np.concatenate([rs, [rad[0]]])
    return thetas, rs

def create_radar_chart(gold_standard, left, right, movement_names, title="Radar Chart with Smooth Arcs", save_path=None):
    """
    Create a radar chart with smooth arcs for biomechanical assessment data.
    
    Parameters:
    - gold_standard: list/array of gold standard values for each movement
    - left: list/array of left side values for each movement  
    - right: list/array of right side values for each movement
    - movement_names: list/array of movement name strings
    - title: string for chart title (optional)
    - save_path: string path to save the chart (optional, if None will show chart)
    
    Returns:
    - fig: matplotlib figure object
    """
    
    # Validate inputs
    if not (len(gold_standard) == len(left) == len(right) == len(movement_names)):
        raise ValueError("All input arrays must have the same length")
    
    num_vars = len(movement_names)
    
    # Prepare data - add first element to end for closed polygon
    Gold_Standard = list(gold_standard) + [gold_standard[0]]
    Left = list(left) + [left[0]]
    Right = list(right) + [right[0]]

    # Find maximum value among Left and Right
    max_val = max(max(Left), max(Right))
    # Ensure axis_array ends at a multiple of 20
    axis_end = ((int(max_val) + 19) // 20) * 20
    axis_array = list(range(20, axis_end + 1, 20))
    
    # Create angles for each movement
    angles = np.linspace(0, 2*np.pi, num_vars, endpoint=False).tolist()
    angles += angles[:1]
    
    # Create the plot with larger figure size to accommodate external labels
    fig = plt.figure(figsize=(10, 10), facecolor='#22223b')
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor("#494a4e")
    ax.set_theta_direction(-1)
    ax.set_theta_zero_location('N')
    
    # Custom grid
    ax.yaxis.grid(True, color='#c9ada7', linestyle='--', lw=1.5, alpha=0.7)
    ax.xaxis.grid(True, color='#c9ada7', linestyle='--', lw=1.5, alpha=0.7)
    ax.spines['polar'].set_visible(False)
    
    # Set up ticks without labels (we'll add custom labels outside)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([])  # Remove default labels
    ax.set_ylim(0,120)
    ax.set_yticks(axis_array)
    ax.set_yticklabels([str(i) for i in axis_array], fontsize=11, color='#c9ada7', zorder=15)
    ax.set_rlabel_position(90)
    
    # Plot curves with fill and shadow
    for data, color, lw, label, fill_color in [
        (Gold_Standard,'#34a853',3,'Gold Standard','#34a85333'),
        (Left,'#4285f4',2,'Left','#4285f433'),
        (Right,'#ea4335',2,'Right','#ea433533')
    ]:
        th, rr = arc_curve(angles, data, points_per_seg=80, bulge=0.1)
        ax.plot(th, rr, color=color, lw=lw, alpha=0.98, label=label, zorder=3)
        ax.fill(th, rr, color=fill_color, alpha=0.5, zorder=2)
    
    # Add scatter points for each data
    for data, color in [
        (Gold_Standard,'#34a853'),
        (Left,'#4285f4'),
        (Right,'#ea4335')
    ]:
        ax.scatter(angles[:-1], data[:-1], color=color, s=80, edgecolor='white', zorder=4, alpha=0.9)
    
    # Add custom labels outside the chart
    label_distance = 120  # Distance from center for labels
    for angle, label in zip(angles[:-1], movement_names):
        # Calculate position for label
        x = label_distance * np.cos(angle - np.pi/2)  # -π/2 because polar chart starts at top
        y = label_distance * np.sin(angle - np.pi/2)
        
        # Convert to data coordinates
        ax.text(angle, label_distance, label, 
               horizontalalignment='center', 
               verticalalignment='center',
               fontsize=12, 
               fontweight='bold', 
               color='#f2e9e4',
               rotation=0,  # Keep text horizontal for better readability
               bbox=dict(boxstyle="round,pad=0.3", facecolor='#22223b', edgecolor='none', alpha=0.8),
               zorder=10)  # Ensure labels appear in front
    
    # Title and legend
    plt.title(title, size=18, pad=30, weight='bold', color="#8f847f")
    plt.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12, frameon=False, labelcolor='white')
    plt.tight_layout()
    
    # Save or show
    if save_path:
        plt.savefig(save_path, facecolor='#22223b', dpi=300, bbox_inches='tight')
        plt.close()
    else:
        plt.show()
    
    return fig

# Example usage:
if __name__ == "__main__":
    
    # Example for shoulder assessment
    shoulder_movements = ['External Rotation', 'Internal Rotation', 'Flexion', 'Extension']
    gold_values = [100, 100, 100, 100]
    left_values = [85, 12, 78, 88]
    right_values = [90, 88, 12, 85]

    fig = create_radar_chart(gold_values, left_values, right_values, shoulder_movements, 
                        title="Shoulder Assessment", save_path="shoulder_assessment_radar_chart.png")