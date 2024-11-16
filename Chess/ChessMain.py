import pygame as p
from Chess import ChessEngine
LATIME = INALTIME = 512
DIM = 8
PATRAT = INALTIME // DIM
FPS = 15
IMAGINI = {}
def Piese():
    piese = ['wp', 'wR', 'wN', 'wB', 'wK', 'wQ', 'bp', 'bR', 'bN', 'bB', 'bK', 'bQ']
    for piesa in piese:
        IMAGINI[piesa] = p.transform.scale(p.image.load("images/" + piesa + ".png"), (PATRAT, PATRAT))
def Joc():
    p.init()
    ecran = p.display.set_mode((LATIME, INALTIME))
    ceas = p.time.Clock()
    ecran.fill(p.Color("white"))
    stare = ChessEngine.GameState()
    mutari = stare.getValidMoves()
    mutare_facuta = False
    Piese()
    in_derulare = True
    selectat = ()
    clickuri = []
    while in_derulare:
        for eveniment in p.event.get():
            if eveniment.type == p.QUIT:
                in_derulare = False
            elif eveniment.type == p.MOUSEBUTTONDOWN:
                locatie = p.mouse.get_pos()
                coloana, rand = locatie[0] // PATRAT, locatie[1] // PATRAT
                selectat = () if selectat == (rand, coloana) else (rand, coloana)
                clickuri = [] if selectat == () else clickuri + [selectat]
                if len(clickuri) == 2:
                    mutare = ChessEngine.Move(clickuri[0], clickuri[1], stare.board)
                    print(mutare.getChessNotation())
                    for i in range(len(mutari)):
                        if mutare == mutari[i]:
                            stare.makeMove(mutari[i])
                            mutare_facuta, selectat, clickuri = True, (), []
                            break
                    if not mutare_facuta:
                        clickuri = [selectat]
            elif eveniment.type == p.KEYDOWN and eveniment.key == p.K_z:
                stare.undoMove()
                mutare_facuta = True
        if mutare_facuta:
            mutari, mutare_facuta = stare.getValidMoves(), False
        StareJoc(ecran, stare)
        ceas.tick(FPS)
        p.display.flip()
def StareJoc(ecran, stare):
    Tabla(ecran)
    PieseJoc(ecran, stare.board)
def Tabla(ecran):
    culori = [p.Color("white"), p.Color("gray")]
    [p.draw.rect(ecran, culori[(r + c) % 2], p.Rect(c * PATRAT, r * PATRAT, PATRAT, PATRAT))
     for r in range(DIM) for c in range(DIM)]
def PieseJoc(ecran, tabla):
    [ecran.blit(IMAGINI[tabla[r][c]], p.Rect(c * PATRAT, r * PATRAT, PATRAT, PATRAT))
     for r in range(DIM) for c in range(DIM) if tabla[r][c] != "--"]
if __name__ == "__main__":
    Joc()