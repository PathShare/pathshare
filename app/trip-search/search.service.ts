import { Injectable } from '@angular/core';
import { Ride } from '../shared/model/ride';
import { Observable } from 'rxjs';
import { HttpClient, HttpHeaders } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class SearchService {

  constructor(private http: HttpClient) { }
//COMMENTED OUT BY KIEN 
  // getAllRides(): Observable<Ride[]> {
  //   return this.http.get<Ride[]>('api/rides');
  // }
}
