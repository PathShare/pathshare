import { TripSearchModule } from './trip-search.module';

describe('TripSearchModule', () => {
  let tripSearchModule: TripSearchModule;

  beforeEach(() => {
    tripSearchModule = new TripSearchModule();
  });

  it('should create an instance', () => {
    expect(tripSearchModule).toBeTruthy();
  });
});
