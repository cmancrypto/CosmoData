import type { NextPage } from 'next';
import Head from 'next/head';
import Link from 'next/link';
import styles from '../styles/Home.module.css';

const Home: NextPage = () => {
  return (
    <div className={styles.container}>
      <Head>
        <title>CosmoData API</title>
        <meta name="description" content="API for querying CosmosSDK blockchain data" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Welcome to <span className={styles.highlight}>CosmoData API</span>
        </h1>

        <p className={styles.description}>
          A powerful API for accessing CosmosSDK blockchain data
        </p>

        <div className={styles.grid}>
          <Link href="/api/chains" className={styles.card}>
            <h2>Chains &rarr;</h2>
            <p>View all available chains.</p>
          </Link>

          <a
            href="https://github.com/yourusername/CosmoData"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.card}
          >
            <h2>Documentation &rarr;</h2>
            <p>Find detailed API documentation on GitHub.</p>
          </a>
        </div>
      </main>

      <footer className={styles.footer}>
        <a
          href="https://github.com/yourusername/CosmoData"
          target="_blank"
          rel="noopener noreferrer"
        >
          Powered by CosmoData
        </a>
      </footer>
    </div>
  );
};

export default Home; 