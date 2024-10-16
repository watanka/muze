import logo from './logo.svg';
import './App.css';
import { useState } from 'react';


function Header(props){
    return <header>
        <h2><a href='/' onClick={(event)=>{
          event.preventDefault();
          props.onChangeMode();
        }}>{props.title}</a></h2>
      </header>
}

function Nav(props){
  const lis = []
  for (let i=0; i<props.topics.length;i++){
    let t = props.topics[i]
    lis.push(<li key={t.id}>
      <a id={t.id} href={'/read/'+t.id} onClick={(event)=>{
        event.preventDefault();
        props.onChangeMode(Number(event.target.id));
      }}>{t.title}</a>
      </li>)
  }
  return <nav> 
  <ol>
    {lis}
  </ol>
</nav>
}

function Article(props){
  return <article>
  <h2>{props.title}</h2>
  {props.body}
</article>
}

function App() {
  const topics = [
    {id:1, title: 'html', body: 'html is ...'},
    {id:2, title: 'css', body: 'css is ...'},
    {id:3, title: 'js', body: 'js is ...'},
  ]
  const [mode, setMode] = useState('WELCOME');
  const [id, setId] = useState(null);
  
  let content = null;
  let title, body = '';
  for (let i=0; i< topics.length;i++){
    if (id === topics[i]['id']){
      title = topics[i]['title'];
      body = topics[i]['body'];
    }
  }

  content = <Article title={title} body={"Hello," + body}></Article>
  return (
    <div>
        <Header title="TITLE" onChangeMode={()=>{
            setMode("WELCOME");
        }}></Header>
        <Nav topics={topics} onChangeMode={(_id) =>{
            setId(_id);
        }}></Nav>
        {content}
    </div>
  );
}

export default App;
