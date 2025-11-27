import tkinter as tk
import numpy as np

# Constants
PIXEL_SIZE = 20
GRID_SIZE = 28
SPACING = 8
CELL_SPACING = 20
LABEL_SPACING = 20
STATUS_PIXEL_SIZE = 8
STATUS_SPACING = 2
MAX_INTENSITY = 255
INCREMENT = 40


W1 = np.load("W1_3.npy")
B1 = np.load("B1_3.npy")
W2 = np.load("W2_3.npy")
B2 = np.load("B2_3.npy")

# Image matrix
Img = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

# Create the main window
root = tk.Tk()
root.title("28x28 Smooth Drawing Grid with Real-Time MNIST")


grid_width = (PIXEL_SIZE + SPACING) * GRID_SIZE
cells_width = (PIXEL_SIZE + SPACING) * 10 + 50
canvas_width = grid_width + cells_width + 50
canvas_height = (PIXEL_SIZE + SPACING) * GRID_SIZE
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg="white")
canvas.pack()


rectangles = {}
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        x1 = j * (PIXEL_SIZE + SPACING)
        y1 = i * (PIXEL_SIZE + SPACING)
        x2, y2 = x1 + PIXEL_SIZE, y1 + PIXEL_SIZE
        rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill="black")
        rectangles[(i, j)] = rect_id


cells_start_x = grid_width + 50
cells_center_x = cells_start_x + (cells_width - (10 * (PIXEL_SIZE + SPACING))) // 2


labels = {}
for i in range(10):
    x = cells_center_x + i * (PIXEL_SIZE + SPACING) + PIXEL_SIZE // 2  # Center of each cell
    y = LABEL_SPACING - 5
    label_id = canvas.create_text(x, y, text=str(i), font=("Arial", 10))
    labels[i] = label_id


y2_cells = {}
for i in range(10):
    x1 = cells_center_x + i * (PIXEL_SIZE + SPACING)
    y1 = LABEL_SPACING
    x2, y2 = x1 + PIXEL_SIZE, y1 + PIXEL_SIZE
    rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="black")
    y2_cells[i] = rect_id


g2_cells = {}
for i in range(10):
    x1 = cells_center_x + i * (PIXEL_SIZE + SPACING)
    y1 = LABEL_SPACING + PIXEL_SIZE + CELL_SPACING
    x2, y2 = x1 + PIXEL_SIZE, y1 + PIXEL_SIZE
    rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="black")
    g2_cells[i] = rect_id


y1_cells = {}
for i in range(10):
    x1 = cells_center_x + i * (PIXEL_SIZE + SPACING)
    y1 = LABEL_SPACING + (PIXEL_SIZE + CELL_SPACING) * 2  # Below G2
    x2, y2 = x1 + PIXEL_SIZE, y1 + PIXEL_SIZE
    rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="black")
    y1_cells[i] = rect_id


g1_cells = {}
for i in range(10):
    x1 = cells_center_x + i * (PIXEL_SIZE + SPACING)
    y1 = LABEL_SPACING + (PIXEL_SIZE + CELL_SPACING) * 3  # Below Y1
    x2, y2 = x1 + PIXEL_SIZE, y1 + PIXEL_SIZE
    rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="black")
    g1_cells[i] = rect_id


status_cells = {}
status_start_x = cells_start_x + (
            cells_width - (GRID_SIZE * (STATUS_PIXEL_SIZE + STATUS_SPACING))) // 2  # Center the status cells
for j in range(GRID_SIZE):
    x1 = status_start_x + j * (STATUS_PIXEL_SIZE + STATUS_SPACING)  # Single row
    y1 = LABEL_SPACING + (PIXEL_SIZE + CELL_SPACING) * 4  # Below G1
    x2, y2 = x1 + STATUS_PIXEL_SIZE, y1 + STATUS_PIXEL_SIZE
    rect_id = canvas.create_rectangle(x1, y1, x2, y2, outline="gray", fill="black")
    status_cells[j] = rect_id


def draw(event):
    col, row = event.x // (PIXEL_SIZE + SPACING), event.y // (PIXEL_SIZE + SPACING)


    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and event.x < grid_width:
        if Img[row, col] < MAX_INTENSITY:
            Img[row, col] = min(Img[row, col] + INCREMENT, MAX_INTENSITY)
            color = f"#{Img[row, col]:02x}{Img[row, col]:02x}{Img[row, col]:02x}"
            canvas.itemconfig(rectangles[(row, col)], fill=color)

        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                nr, nc = row + dr, col + dc
                if 0 <= nr < GRID_SIZE and 0 <= nc < GRID_SIZE:
                    if (nr, nc) != (row, col):
                        Img[nr, nc] = min(Img[nr, nc] + INCREMENT // 2, MAX_INTENSITY)
                        color = f"#{Img[nr, nc]:02x}{Img[nr, nc]:02x}{Img[nr, nc]:02x}"
                        canvas.itemconfig(rectangles[(nr, nc)], fill=color)

        update_status_cells()
        update_g1_cells()
        update_y1_cells()
        update_g2_cells()
        update_y2_cells()



def clear_drawing():
    global Img
    Img = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)

    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            canvas.itemconfig(rectangles[(i, j)], fill="black")

    for col in range(GRID_SIZE):
        canvas.itemconfig(status_cells[col], fill="black")


    for i in range(10):
        canvas.itemconfig(g1_cells[i], fill="black")
        canvas.itemconfig(y1_cells[i], fill="black")
        canvas.itemconfig(g2_cells[i], fill="black")
        canvas.itemconfig(y2_cells[i], fill="black")



def update_status_cells():
    for col in range(GRID_SIZE):
        avg_brightness = np.mean(Img[:, col])
        color = f"#{int(avg_brightness):02x}{int(avg_brightness):02x}{int(avg_brightness):02x}"
        canvas.itemconfig(status_cells[col], fill=color)



def normalize_for_display(arr):
    arr_min, arr_max = np.min(arr), np.max(arr)
    if arr_max == arr_min:
        return np.zeros_like(arr)
    return ((arr - arr_min) / (arr_max - arr_min) * MAX_INTENSITY).astype(int)



def update_g1_cells():

    Img_normalized = Img / MAX_INTENSITY
    Img2 = np.reshape(Img_normalized, (1, 784)).T
    G1 = np.dot(W1, Img2) + B1
    print("G1 values:", G1.flatten())  # Debug print
    G1_normalized = normalize_for_display(G1)  # Normalize for display
    for i in range(10):
        intensity = int(G1_normalized[i, 0])
        color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
        canvas.itemconfig(g1_cells[i], fill=color)



def update_y1_cells():

    Img_normalized = Img / MAX_INTENSITY
    Img2 = np.reshape(Img_normalized, (1, 784)).T
    G1 = np.dot(W1, Img2) + B1
    Y1 = np.maximum(G1, 0)
    print("Y1 values:", Y1.flatten())
    Y1_normalized = normalize_for_display(Y1)
    for i in range(10):
        intensity = int(Y1_normalized[i, 0])
        color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
        canvas.itemconfig(y1_cells[i], fill=color)



def update_g2_cells():
    Img_normalized = Img / MAX_INTENSITY
    Img2 = np.reshape(Img_normalized, (1, 784)).T
    G1 = np.dot(W1, Img2) + B1
    Y1 = np.maximum(G1, 0)
    G2 = np.dot(W2, Y1) + B2
    print("G2 values:", G2.flatten())
    G2_normalized = normalize_for_display(G2)
    for i in range(10):
        intensity = int(G2_normalized[i, 0])
        color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
        canvas.itemconfig(g2_cells[i], fill=color)



def update_y2_cells():
    Img_normalized = Img / MAX_INTENSITY
    Img2 = np.reshape(Img_normalized, (1, 784)).T
    G1 = np.dot(W1, Img2) + B1
    Y1 = np.maximum(G1, 0)
    G2 = np.dot(W2, Y1) + B2
    Y2 = SoftMax(G2)
    print("Y2 values (before scaling):", Y2.flatten())
    Y2 = Y2 * MAX_INTENSITY
    Y2 = np.clip(Y2, 0, MAX_INTENSITY)
    print("Y2 values (after scaling):", Y2.flatten())
    for i in range(10):
        intensity = int(Y2[i, 0])
        color = f"#{intensity:02x}{intensity:02x}{intensity:02x}"
        canvas.itemconfig(y2_cells[i], fill=color)



def SoftMax(A):
    return np.exp(A) / np.sum(np.exp(A), axis=0, keepdims=True)


clear_button = tk.Button(root, text="Clear", command=clear_drawing)
clear_button.pack(pady=10)

canvas.bind("<B1-Motion>", draw)

root.mainloop()