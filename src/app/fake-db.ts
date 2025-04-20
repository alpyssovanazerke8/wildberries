import {Post} from './models';

export const POSTS: Post[] = [];


for (let i = 1; i <= 10; i++) {
  POSTS.push(
    {
      id: i,
      title: `Title ${i}`,
      body: `Lorem ipsum dolor sit amet, consectetur adipisicing elit. Cupiditate debitis iste nihil non quia? Atque dolorem illo inventore officia quas totam voluptatum. Ad aliquid consequuntur eum ipsa magni non, qui?`,
    }
  )
}
