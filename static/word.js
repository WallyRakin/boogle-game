class Word {
    constructor(board, currentCell) {
        this.board = board;
        this.rowLength = board.length;
        this.colLength = board[0].length;

        let [y, x] = currentCell.split('-');
        this.word = `${board[y][x]}`;
        this.cellsSeen = [currentCell,];
        this.currentCell = currentCell;
        this.originCell = '';
        this.possibleCells = this._computePossibleCells(Number(x), Number(y));
    }
    _computePossibleCells(x, y) {
        let possibleCells = [];
        // console.log(typeof x)
        if ((x - 1) >= 0) {
            // console.log('x-1');
            possibleCells.push(`${y}-${x - 1}`)
            if ((y - 1) >= 0) {
                // console.log('x-1,y-1');
                possibleCells.push(`${y - 1}-${x - 1}`)
            };
            if ((y + 1) < 5) {
                // console.log('x-1,y+1');
                possibleCells.push(`${y + 1}-${x - 1}`);
            };
        };
        if ((x + 1) < 5) {
            // console.log('x+1');
            possibleCells.push(`${y}-${x + 1}`);
            if ((y - 1) >= 0) {
                // console.log('x+1,y-1');
                possibleCells.push(`${y - 1}-${x + 1}`)
            };
            if ((y + 1) < 5) {
                // console.log('x+1,y+1');
                possibleCells.push(`${y + 1}-${x + 1}`);
            };
        };
        if ((y - 1) >= 0) {
            // console.log('y-1');
            possibleCells.push(`${y - 1}-${x}`)
        };
        if ((y + 1) < 5) {
            // console.log('y+1');
            possibleCells.push(`${y + 1}-${x}`);
        };
        possibleCells = possibleCells.filter(a => { return !(this.cellsSeen.includes(a)) });
        // console.log(possibleCells);
        return possibleCells;
    };

    _updateCurrentCell(cell) {
        let [y, x] = cell.split('-');
        this.originCell = this.currentCell;
        this.cellsSeen.push(cell);
        this.currentCell = cell;
        this.word += this.board[y][x];
        this.possibleCells = this._computePossibleCells(Number(x), Number(y));
    };

    checkcell(cell) {
        // console.log(this.possibleCells)
        // console.log(cell);
        if (!(this.possibleCells.includes(cell))) { return };
        // console.log('updated');

        this._updateCurrentCell(cell);
        return 'pass';
    };

    submitWord() {
        this.possibleCells = [];
        return this.word.toLocaleLowerCase();
    }
}
