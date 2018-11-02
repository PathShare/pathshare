export interface Coordinate {latitude: number; longitude: number; }

export class Ride {
    id: number;
    // TODO: SB-Create_Trip_Search - add riders as User[]
    departureDate: Date;
    seatPrice: number;
    departureLocation: Coordinate;
    destinationLocation: Coordinate;
    active: boolean;
}
