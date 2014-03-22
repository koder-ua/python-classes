import os
import sys
import os.path

from PySide import QtGui, QtCore

from chess_base import board_letters, to_str_pos, to_tuple_pos, is_valid_cell
from chess import Pawn, Rook, Knight, King, Queen, Bishop, Board, knorre_vs_neumann

self_dir = os.path.dirname(os.path.join(os.getcwd(), sys.argv[0]))

class Example(QtGui.QWidget):
    
    board_text_space = 15
    min_board_sz = 80
    hit_cell_color = "red"
    move_cell_color = "green"
    hit_and_move_cell_color = "orange"
    piece_cell_color = "yellow"

    img_path = os.path.join(self_dir, "chess_piece")

    piece_fname_mapping = {
        "WQ": "white_quinn",
        "WK": "white_king",
        "WP": "white_pawn",
        "WN": "white_knight",
        "WR": "white_rook",
        "WB": "white_bishop",
        "BQ": "black_quinn",
        "BK": "black_king",
        "BP": "black_pawn",
        "BN": "black_knight",
        "BR": "black_rook",
        "BB": "black_bishop",
    }

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()
        self.font = QtGui.QFont("times", 24)
        self.chess_piece_font = QtGui.QFont("console", 30)
        self.fm = QtGui.QFontMetrics(self.font)
        self.chess_piece_fm = QtGui.QFontMetrics(self.chess_piece_font)
        self.vertical_lines_x_corrds = []
        self.horizontal_lines_y_coords = []

        self.board = Board(knorre_vs_neumann())

        self.pieces_images = {}
        self.load_pieces(self.img_path)

        self.active_cell = None
        self.selected_piece = None

    def cell_to_coords(self, cell):
        return self.cell_index_to_coords(*to_tuple_pos(cell))

    def cell_index_to_coords(self, cell_x, cell_y):
        cell_y = 7 - cell_y
        x1, x2 = self.vertical_lines_x_corrds[cell_x: cell_x + 2]
        y1, y2 = self.horizontal_lines_y_coords[cell_y: cell_y + 2]
        return x1, y1, x2 - x1, y2 - y1

    def load_pieces(self, path):
        for key, fname in self.piece_fname_mapping.items():
            img = QtGui.QImage()
            img.load(os.path.join(path, fname))
            self.pieces_images[key] = img

    def initUI(self):      
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Chess GUI')
        self.show()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.draw_board(qp)

    def get_cell_from_abs_pos(self, x, y):
        if x < self.vertical_lines_x_corrds[0] or x > self.vertical_lines_x_corrds[-1]:
            return False, None, None

        if y < self.horizontal_lines_y_coords[0] or y > self.horizontal_lines_y_coords[-1]:
            return False, None, None

        for xpos, cx in enumerate(self.vertical_lines_x_corrds[1:]):
            if x < cx:
                break

        for ypos, cy in enumerate(self.horizontal_lines_y_coords[1:]):
            if y < cy:
                break

        return True, xpos, 7 - ypos

    def mousePressEvent(self, event):
        ok, xpos, ypos = self.get_cell_from_abs_pos(event.pos().x(), event.pos().y())
        if ok:
            piece = self.board.get((xpos, ypos))
            if piece is not None:
                self.selected_piece = piece
            else:
                self.selected_piece = None
        else:
            return super(Example, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):
        if self.selected_piece is not None:
            ok, xpos, ypos = self.get_cell_from_abs_pos(event.pos().x(), event.pos().y())
            if ok:
                #piece = self.board.get((xpos, ypos))
                self.board.move(self.selected_piece, (xpos, ypos))
            else:
                self.selected_piece = None
            self.repaint()
        else:
            return super(Example, self).mouseReleaseEvent(event)

    def mouseReleaseEvent(self, event):
        ok, xpos, ypos = self.get_cell_from_abs_pos(event.pos().x(), event.pos().y())
        self.selected_piece = None

        if ok:
            self.on_cell_clicked(xpos, ypos)
        else:
            return super(Example, self).mouseReleaseEvent(event)

    def on_cell_clicked(self, xpos, ypos):
        self.active_cell = (xpos, ypos)
        self.repaint()

    def draw_board(self, painter):

        # calculate sizes
        sz = self.geometry().size()
        painter.setFont(self.font)

        text_h = self.fm.height()
        text_w = max(map(self.fm.width, "12345678"))

        board_sz = min(sz.height() - text_h - self.board_text_space * 3, 
                       sz.width() - text_w - self.board_text_space * 3)

        board_and_text_w = text_w + self.board_text_space + board_sz
        board_and_text_h = text_h + self.board_text_space + board_sz

        y_start_pos = (sz.height() - board_and_text_h) / 2
        x_start_pos = (sz.width() - board_and_text_w) / 2

        step = float(board_sz) / 8
        half_step = int(step / 2)

        self.horizontal_lines_y_coords = [y_start_pos + int(i * step) for i in range(9)]
        vertical_start_x = x_start_pos + text_w + self.board_text_space
        self.vertical_lines_x_corrds = [vertical_start_x + int(i * step) for i in range(9)]

        # draw labels
        for text, curr_y in zip("87654321", self.horizontal_lines_y_coords[:-1]):
            painter.drawText(x_start_pos, curr_y + half_step + text_h / 2, text)
            #painter.drawRect(x_start_pos, curr_y - text_h, text_w, text_h)

        curr_y = y_start_pos + board_and_text_h - text_h / 2
        for text, curr_x in zip(board_letters, self.vertical_lines_x_corrds[:-1]):
            painter.drawText(curr_x + half_step - self.fm.width(text) / 2, curr_y, text)

        # draw black squares
        self.set_color(painter, lambda x, y: (x + y) % 2 == 1, "grey")

        for piece in self.board:
            tp, move, hit = piece.full_name(), self.board.get_all_moves(piece), self.board.get_all_hits(piece)

            if piece.pos == self.active_cell:
                hit = list(hit)
                move = list(move)
                #print "hit =", hit

                move = map(to_tuple_pos, move)
                hit = map(to_tuple_pos, hit)

                self.draw_piece(painter, piece.pos, tp, list(move), list(hit), True)                
            else:
                self.draw_piece(painter, piece.pos, tp, "", "", False)

        self.draw_grid(painter, x_start_pos + text_w + self.board_text_space, y_start_pos, board_sz)

    def to_colored(self, piece):
        if piece[0] == "W":
            return self.white(piece[1:])
        else:
            assert piece[0] == "B"
            return self.black(piece[1:])

    def white(self, piece):
        return unicode(piece) + U"\u21D1"

    def black(self, piece):
        return unicode(piece) + U"\u21D3"

    def draw_piece(self, painter, pos, text, move_cells, hit_cells, collor_under_piece=False, use_image=True):

        hit_cells_set = set(hit_cells)
        move_cells_set =  set(move_cells)
        
        hit_only = hit_cells_set - move_cells_set
        move_only = move_cells_set - hit_cells_set
        hit_and_move = move_cells_set & hit_cells_set

        self.set_color(painter, list(hit_only), self.hit_cell_color, 125)
        self.set_color(painter, list(move_only), self.move_cell_color, 125)
        self.set_color(painter, list(hit_and_move), self.hit_and_move_cell_color, 125)

        if collor_under_piece:
            self.set_color(painter, [pos], self.piece_cell_color, 125)

        cell_x, cell_y = pos

        if not use_image:
            c = "white" if (cell_x + cell_y) % 2 == 1 else "black"
            self.draw_text(painter, pos, self.to_colored(text), c)
        else:
            x, y, w, h = self.cell_to_coords(pos)
            painter.drawImage(x + h * 0.05, y + h * 0.05, 
                              self.pieces_images[text].scaledToHeight(h * 0.9, QtCore.Qt.SmoothTransformation))


    def draw_text(self, painter, cell, text, color):
        c = QtGui.QColor(color)
        x, y, w, h = self.cell_to_coords(cell)
        painter.setFont(self.chess_piece_font)
        painter.setPen(c)
        painter.drawText(x + w / 2 - self.chess_piece_fm.width(text) / 2, 
                         y + h / 2 + self.chess_piece_fm.height() / 3, text)
        painter.setFont(self.font)
        painter.setPen(QtGui.QColor("black"))

    def draw_grid(self, painter, x_start, y_start, board_sz):
        # draw lines
        y_pairs = zip(self.horizontal_lines_y_coords[:-1], self.horizontal_lines_y_coords[1:])
        for y in self.horizontal_lines_y_coords:
            painter.drawLine(x_start, y, x_start + board_sz, y)

        for x in self.vertical_lines_x_corrds:
            painter.drawLine(x, y_start, x, y_start + board_sz)


    def set_color(self, painter, filter_func, color, alpha=255):
        if isinstance(filter_func, list):
            if len(filter_func) == 0:
                return

            filter_array = filter_func
            filter_func = lambda x, y: (x, y) in filter_array

        c = QtGui.QColor(color)
        c.setAlpha(alpha)

        for x_cell_p in range(8):
            for y_cell_p in range(8):
                if filter_func(x_cell_p, y_cell_p):
                    x, y, w, h = self.cell_index_to_coords(x_cell_p, y_cell_p)
                    painter.fillRect(x, y, w, h, c)

        #if board_sz <= self.min_board_sz:
        #    return
        
        #text_starts_at_x = board_sz + board_text_space
        #text_starts_at_y = 
        #print sz
        #self.drawText(event, qp)
        #qp.end()
        #qp.setPen(QtGui.QColor(168, 34, 3))
        #qp.setFont(QtGui.QFont('Decorative', 10))
        #qp.drawText(event.rect(), QtCore.Qt.AlignCenter, self.text)        
        
                
        
def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
