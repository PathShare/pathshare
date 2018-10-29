import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Ride } from './model/ride';


export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const rides = [
      { id: 1, departureDate: new Date(), seatPrice: 20, departureLocation: {latitude: 0.0, longitude: 0.0},
        destinationLocation: {latitude: 0.0, longitude: 0.0}, active: true}
    ];
    return {rides};
  }

  // Overrides the genId method to ensure that a hero always has an id.
  // If the heroes array is empty,
  // the method below returns the initial number (11).
  // if the heroes array is not empty, the method below returns the highest
  // hero id + 1.
  genId(rides: Ride[]): number {
    return rides.length > 0 ? Math.max(...rides.map(hero => hero.id)) + 1 : 1;
  }
}
