package student_player;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

import boardgame.Board;
import pentago_twist.PentagoBoardState;
import pentago_twist.PentagoMove;


public class MyTools {
    
    public static class Node {
    	
    	// ATTRIBUTES //

        private PentagoBoardState state;
        private PentagoMove move;
        private Node parent;
        private ArrayList<Node> children = new ArrayList<>();
        private int visitCount = 0;
        private double score = 0;

        // CONSTRUCTORS //
        
        public Node() {
        }
        
        public Node(PentagoBoardState state, PentagoMove move, Node parent) {
            this.state = state;
            this.move = move;
            this.parent = parent;
        }
        
        // STATE RELATED FUNCTIONS // 
        
        public PentagoBoardState getState() {
        	return this.state;
        }
        
        public void setState(PentagoBoardState state) {
        	this.state = state;
        }
        
        // SCORE RELATED FUNCTIONS //

        public void updateStats(double score) {
        	this.visitCount++;
        	this.score += score;
        }
        
        public void setScore(double score) {
        	this.score = score;
        }
        
        public double getScore() {
        	return this.score;
        }
        
        // PARENT RELATED FUNCTIONS //
        
        public void setNullParent() {
        	this.parent = null;
        }
        
        public Node getParent(){
        	return this.parent;
        }
        
        // WINNER RELATED FUNCTION //
        
        public boolean hasWinner() {
        	if (this.getState().getWinner()==Board.NOBODY) {
        		return false;
        	} else {
        		return true;
        	}
        }
        
        // CHILDREN RELATED FUNCTIONS //
        
        public ArrayList<Node> getChildren(){
        	return this.children;
        }
        
        public void addChild(Node child) {
        	this.children.add(child);
        }
        
        public boolean hasChildren() {
        	if (this.getChildren().size()>0) {
        		return true;
        	} else {
        		return false;
        	}
        }
        
        public Node bestChild() {
        	return Collections.max(this.children, Comparator.comparing(c -> c.getScore()));
        }
        
        public Node randomChild(){
            return this.children.get((int)Math.random()*this.children.size());
        }
        
        public Node childWithState(PentagoBoardState state) {
        	for(Node child: this.getChildren()) {
        		if(isSame(child.getState(),state)) {
        			return child;
        		}
        	} 
        	return null;
        }
        
        public boolean isSame(PentagoBoardState board1, PentagoBoardState board2) {
        	if (board1==board2) return true;
        	if (board1.getBoard()!=board2.getBoard()) return false;
        	if(board1.getTurnPlayer()!=board2.getTurnPlayer()) return false;
        	if(board1.getWinner()!=board2.getWinner()) return false;
        	if(board1.getTurnNumber()!=board2.getTurnNumber()) return false;
        	return true;
        }
      
        
        // MOVE RELATED FUNCTION //
        
        public PentagoMove getMove() {
        	return this.move;
        }
        
        // VISIT COUNT RELATED FUNCTION //
        
        public int getVisitCount() {
        	return this.visitCount;
        }
        
        
        // MONTECARLO TREE SEARCH FUNCTIONS // 
        
        
        /*
         * returns a potentially good node with maximum uct value
         */
        public Node getPotentiallyGood() {
            Node node = this;
            while (!node.children.isEmpty()) {
                node = node.best_uct();
            }
            return node;
        }
        
        /*
         * Apply legal moves to create child states
         */
        public void expand() {
        	long startTime = System.currentTimeMillis();
            for (PentagoMove move: this.getState().getAllLegalMoves()) {
            	if((System.currentTimeMillis()-startTime)>=1000 && this.getState().getTurnNumber()==1) {
            		break;
            	}
            	PentagoBoardState childState = (PentagoBoardState) this.getState().clone();
            	childState.processMove(move);
            	Node child = new Node (childState, move, this);
            	this.addChild(child);
            }
        }
        
        /*
         * Simulate game until terminal state is reached
         */
        public int simulate(int opponent) {
            PentagoBoardState state = (PentagoBoardState) this.getState().clone();
            if (opponent == state.getWinner()) {
                this.getParent().setScore(Integer.MIN_VALUE);
                return opponent;
            }
            if ((1-opponent) == state.getWinner()) {
                this.getParent().setScore(Integer.MAX_VALUE);
                return (1-opponent);
            }
            PentagoMove move;
            while (state.getWinner() == Board.NOBODY) {
                move = (PentagoMove) state.getRandomMove();
                state.processMove(move);
            }
            return state.getWinner();
        }
        
        /*
         * Update the statistics after the simulation
         */
        public void backpropagate(int current, int winner) {
            Node previous = this;
            while (previous != null) {
            	if(winner == current) {
            		previous.updateStats(100);
            	} else {
            		previous.updateStats(0);
            	}
                previous = previous.getParent();
            }
        }
        
        
        // UCT FUNCTIONS //
        
    	public double compute_uct(double wins, double allSim, double currentSim) {
    		return (wins/(currentSim)) + Math.sqrt(2)*Math.sqrt(Math.log(allSim)/(currentSim));
    		
    	}
    	
    	public Node best_uct() {
    		Node best = Collections.max(this.getChildren(),Comparator.comparing(c-> c.compute_uct(c.getScore(),this.getVisitCount(),c.getVisitCount())));
    		return best;
    	}
    }
}