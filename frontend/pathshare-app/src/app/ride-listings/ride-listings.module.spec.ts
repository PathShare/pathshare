import { RideListingsModule } from './ride-listings.module';

describe('RideListingsModule', () => {
  let rideListingsModule: RideListingsModule;

  beforeEach(() => {
    rideListingsModule = new RideListingsModule();
  });

  it('should create an instance', () => {
    expect(rideListingsModule).toBeTruthy();
  });
});
