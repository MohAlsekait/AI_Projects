import java.util.Date;

public class Minmax extends OthelloPlayer {

	public Minmax(String name) {
		super(name);
	}

	@Override
	public Square getMove(GameState currentState, Date deadline) {
	
		GameState s = (GameState)currentState.clone();
		Square mymove = null;
		
		GameState.Player max = s.getCurrentPlayer();
		int r[] = new int[3];
		int result[] = minmax(s, 5, max, r);
		mymove = new Square(result[1], result[2]);
	
		return mymove;	
	}
	
	public int[] minmax(GameState s, int depth, GameState.Player max, int[] r) {
		if(depth == 0||s.getCurrentPlayer()==GameState.Player.EMPTY||s.getStatus()==GameState.GameStatus.PLAYER1WON
				||s.getStatus()==GameState.GameStatus.PLAYER2WON||s.getStatus()==GameState.GameStatus.TIE) {
			
			r[0] = s.getScore(max) ; r[1] = s.getPreviousMove().getRow(); r[2] = s.getPreviousMove().getCol();
			return r;
		}
		
		if(max == s.getCurrentPlayer()) {
			r[0] = Integer.MIN_VALUE;
			for(GameState i: s.getSuccessors()) {
				r[0] = Math.max(r[0], minmax(i, depth-1, max, r)[0]); r[1] = i.getPreviousMove().getRow(); r[2] = i.getPreviousMove().getCol();			
			}
			return r;			
		}
		
		else {
			r[0] = Integer.MAX_VALUE;
			for(GameState i: s.getSuccessors()) {				
				r[0] = Math.min(r[0], minmax(i, depth-1, max, r)[0]); r[1] = i.getPreviousMove().getRow(); r[2] = i.getPreviousMove().getCol();			
			}
			return r;
		}
	}	
}
