export class ShareMyTripService {

    shareMyTrip(startingLocation: string, destinationLocation: string, inputDate: Date, numOfSeats: number, price: number) {
        //sign up the user using backend
        console.log(startingLocation,destinationLocation,inputDate.toLocaleString(),numOfSeats,price)
    }
} 