import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';

import { Observable, of } from 'rxjs';
import { catchError, map, tap } from 'rxjs/operators';

import { Course } from './hero';
// import { MessageService } from './message.service';


@Injectable({ providedIn: 'root' })
export class HeroService {
  private hello;
  private c:Course[] = [];
  private heroesUrl = 'http://127.0.0.1:7000/courses';  // URL to web api

  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  constructor(
    private http: HttpClient) { }

  // testService(){
  //   return this.http.get("http://127.0.0.1:7000/courses").subscribe(
  //     data=>{ this.hello=data;
  //             // console.log(this.hello);
  //             this.hello.forEach(element => {
  //               let tc = new Course();
  //             this.c.push(Object.assign(tc, element));
  //             });
  //             return (this.c);
  //    }
  //   );
  // }
  /** GET heroes from the server */
  getHeroes (): Observable<Course[]> {
    return this.http.get<Course[]>(this.heroesUrl);
  }

  uploadDoc(id, fileToUpload){
    const formData: FormData = new FormData();
    formData.append('id',id);
    formData.set('fileKey', fileToUpload, fileToUpload.name);
    // console.log(formData);
    const headers = new HttpHeaders();
        headers.append('Content-Type', 'multipart/form-data');
        headers.append('Accept', 'application/json');
    return this.http.post(`http://127.0.0.1:7000/fupload`,formData);
  }

  searchDoc(queryStr: String,start,end){
      return this.http.get(`http://127.0.0.1:7000/suggest?query=${queryStr}&start=${start}&end=${end}`);
  }

  categoriseDoc(fileToUpload){
    const formData: FormData = new FormData();
    formData.set('fileKey', fileToUpload, fileToUpload.name);
    // console.log(formData);
    const headers = new HttpHeaders();
        headers.append('Content-Type', 'multipart/form-data');
        headers.append('Accept', 'application/json');
    return this.http.post(`http://127.0.0.1:7000/categorise`,formData);
  }
  getHero(id: number): Observable<Course> {
    const url = `http://127.0.0.1:7000/courseinfo?id=${id}`;
    return this.http.get<Course>(url);
  }

  longPoll(id: number): Observable<Course> {
    const url = `http://127.0.0.1:7000/long_poll?id=${id}`;
    return this.http.get<Course>(url);
  }

  /* GET heroes whose name contains search term */
  searchHeroes(term: string): Observable<Course[]> {
    if (!term.trim()) {
      // if not search term, return empty hero array.
      return of([]);
    }
    return this.http.get<Course[]>(`${this.heroesUrl}/?name=${term}`).pipe(
      tap()
    );
  }
y


}
