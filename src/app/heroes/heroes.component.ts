import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Course } from '../hero';
import { HeroService } from '../hero.service';

@Component({
  selector: 'app-heroes',
  templateUrl: './heroes.component.html',
  styleUrls: ['./heroes.component.css']
})
export class HeroesComponent implements OnInit {
  heroes: Course[];
  documents: any;
  prev_len: any;
  loading: boolean;
  offset: number;
  constructor(private route: ActivatedRoute,private heroService: HeroService, private router:Router) { }

  ngOnInit() {
    this.getHeroes();
    this.loading = false;
    this.offset = 7;
    this.documents = this.heroService.searchDoc("",0,7).subscribe(data=>{
    this.documents = data;
    })
  }

  fileUpload(fileInput: any): void{
    const id = +this.route.snapshot.paramMap.get('id');
    if (fileInput.target.files && fileInput.target.files[0]){
      this.loading = true;
      this.heroService.categoriseDoc(fileInput.target.files[0]).subscribe(data=>{
        this.router.navigate(['/detail/'+data]);
        this.loading =  false;
      });
    }
  }
  loadData(){
    this.heroService.searchDoc("",this.offset,this.offset+5).subscribe(data=>{
      this.offset+=5;
      for(let i=0;i<5;++i)
      {
      if(data[i]){
          this.documents.push(data[i]);
        }
        }
    })
  }
  getHeroes(): void {
    this.heroService.getHeroes()
    .subscribe(heroes => this.heroes = heroes);
  }

  search(name: String){
    name = name.trim();
    this.documents = [];
    if(name=="" || name.length>=2){
      this.heroService.searchDoc(name,0,5).subscribe(
      data=>{
        this.documents = data;
        console.log(data);
      }
    );
  }
}

}
