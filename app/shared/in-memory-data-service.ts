import { InMemoryDbService } from 'angular-in-memory-web-api';
import { Ride } from './model/ride';


export class InMemoryDataService implements InMemoryDbService {
  createDb() {
    const rides = [
      { id: 1, departureDate: new Date(), seatPrice: 20, departureLocation: {latitude: 33.5779, longitude: -101.8552},
        destinationLocation: {latitude: 32.7767, longitude: -96.7970}, active: true}
    ];
    return {rides};
  }

  // Overrides the genId method to ensure that a hero always has an id.
  // If the array is empty,
  // the method below returns the initial number (11).
  // if the array is not empty, the method below returns the highest
  // hero id + 1.
  genId(rides: Ride[]): number {
    return rides.length > 0 ? Math.max(...rides.map(hero => hero.id)) + 1 : 1;
  }
}
