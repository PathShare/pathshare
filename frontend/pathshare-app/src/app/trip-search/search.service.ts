import { Injectable } from '@angular/core';
import { Ride } from '../shared/model/ride';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

// TODO SB-Display_Trip_Listings - move this to shared folder
@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(private http: HttpClient) { }

  getAllRides(): Observable<Ride[]> {
    return this.http.get<Ride[]>('api/rides');
  }

  /**
   * @description gets all rides with a specified departure, destination,
   * and starting date
   */
  getRides(departure: string, destination: string, startDate: string): Observable<Ride[]> {
    return this.http.get<Ride[]>
    (`api/rides/?departure=${departure}&destination=${destination}&departureDate=${startDate}`);
  }
}
