import { Rider } from './rider';

export interface Coordinate {latitude: number; longitude: number; }

export class Ride {
    id: number;
    departureDate: string;
    seatPrice: number;
    departure: string;
    destination: string;
    departureLocation: Coordinate;
    destinationLocation: Coordinate;
    active: boolean;
    riders: Rider[];
}
