package controller;

import model.*;

public class Rules {
    private Game game;

    public Rules(Game game) {
        this.game = game;
    }

    public boolean isRightRange(Card start, Card end) {
        return Math.abs(end.getmX() - start.getmX()) <= 1 && Math.abs(end.getmY() - start.getmY()) <= 1;
    }

    public boolean isToEarth(Card start, Card end) {
        return !start.hasShip() || (start.hasShip() && (Math.abs(end.getmX() - start.getmX()) + Math.abs(end.getmY() - start.getmY())) != 2);
    }

    public boolean isRightSeaMoves(Card start, Card end) {
        return end.getCardType() != CardType.SEA || end.getCardType() == CardType.SEA && ((start.getCardType() == CardType.SEA && !start.hasShip()) || end.hasShip());
    }

    public boolean isValidShipTurn(Ship ship, Card card) {
        if (isRightRange(ship.getCard(), card))
            if (ship.getCard() != card) {
                if (card.getCardType() == CardType.SEA)
                    return true;
            }
        return false;
    }

    public boolean isValidPirateTurn(Pirate pirate, Card card) {
        if (isRightRange(pirate.getCard(), card))
            if (pirate.getCard() != card || pirate.getSleep() != 0) {
                if (isRightSeaMoves(pirate.getCard(), card)) {
                    if (isToEarth(pirate.getCard(), card))
                        if (checkStartCardRule(pirate.getCard(), card, pirate))
                            if (checkEndCardRule(pirate.getCard(), card, pirate))
                                return true;
                }
            }
        return false;
    }

    public boolean isCompleteTurn(Card card) {
        return card.getCardType() != CardType.ARROW
                && card.getCardType() != CardType.HORSE;
    }

    public boolean checkEndCardRule(Card start, Card end, Pirate pirate) {
        switch (end.getCardType()) {
            case JUNGLE:
            case DESERT:
            case BOG:
            case MOUNTAINS:
                return end.getPirates().size() <= 0 || end.getPirates().indexOf(pirate) != -1;
            case FORT:
                if (!end.getPirates().isEmpty()) {
                    return end.getPirates().get(0).getColor().equals(pirate.getColor());
                } else {
                    return true;
                }
            default:
                return true;
        }
    }

    public boolean checkStartCardRule(Card start, Card end, Pirate pirate) {
        Card previousCard = pirate.getPreviousCard();
        switch (start.getCardType()) {
            case JUNGLE:
            case DESERT:
            case BOG:
            case MOUNTAINS:
                if (pirate.getSleep() > 0) {
                    if (start != end) {
                        return false;
                    } else {
                        return true;
                    }
                } else {
                    return true;
                }
            case ARROW:
                return (Math.abs(end.getmX() - start.getmX()) + Math.abs(end.getmY() - start.getmY())) != 2;
            case ICE:
                return end.getmX() == (start.getmX() + start.getmX() - previousCard.getmX()) && end.getmY() == (start.getmY() + start.getmY() - previousCard.getmY());
            case HOLE:
                return !pirate.isInHole();
            default:
                if (pirate.isHaveMoney()) {
                    return end.isOpen();
                } else {
                    return true;
                }


        }

    }
}