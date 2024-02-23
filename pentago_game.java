package student_player;

import boardgame.Move;
import pentago_twist.PentagoMove;
import pentago_twist.PentagoPlayer;
import pentago_twist.PentagoBoardState;
import student_player.MyTools.Node;

public class StudentPlayer extends PentagoPlayer {

    private static final long trainingTime = 2000; // don't change this
    private static final long executionTime = 1900;
    boolean first = true;
    private Node root = new Node();

    public StudentPlayer() {
        super("*********");
    }


    public Move chooseMove(PentagoBoardState boardState) {
    	long start = System.currentTimeMillis();
    	int opponent = 1-boardState.getTurnPlayer();
    	long stopTime;
        if (first) {
            stopTime = start + trainingTime;
            first = false;
        } else {
            stopTime = start + executionTime;
            Node update = root.childWithState(boardState);
            if (update == null) {
            	root = new Node();
            } else {
            	root = update;
            	root.setNullParent();
            }
        }
        root.setState(boardState);
        while (System.currentTimeMillis() < stopTime) {
        	
        	// selection
            Node potentiallyGood = root.getPotentiallyGood();
            
            long expandStartTime = System.currentTimeMillis();
            // expansion
            if (!potentiallyGood.hasWinner()) {
            	if(expandStartTime-start >= 1800 && first==false) {
            		potentiallyGood.expand();
            	} 
            }
            
            // simulation and back-propagation
            if(potentiallyGood.hasChildren()) {
            	Node rChild = potentiallyGood.randomChild();
            	int playout = rChild.simulate(opponent);
            	rChild.backpropagate((1-opponent),playout);
            } else {
            	int playout = potentiallyGood.simulate(opponent);
            	potentiallyGood.backpropagate((1-opponent), playout);
            }
        }
        
        Node best = root.bestChild();
        root = best;
        root.setNullParent();

        PentagoMove myMove = best.getMove();

        return myMove;
    }


}