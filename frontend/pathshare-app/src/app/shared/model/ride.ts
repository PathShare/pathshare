export interface Coordinate {latitude: number; longitude: number; }

export class Ride {
    id: number;
    // TODO: SB-Create_Trip_Search - add riders as User[]
    departureDate: string;
    seatPrice: number;
    departure: string;
    destination: string;
    departureLocation: Coordinate;
    destinationLocation: Coordinate;
    active: boolean;
}
