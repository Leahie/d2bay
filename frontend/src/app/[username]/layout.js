import { Suspense } from 'react';
import Nav from '@/components/Nav';

export default function layout({
    children,
}){
    return (
        <section>
        <Nav page = {1} />
        <div className="box">
            {children}
        </div>
        </section>
    )
}