import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

type FeatureItem = {
  title: string;
  Svg: React.ComponentType<React.ComponentProps<'svg'>>;
  description: JSX.Element;
};

const FeatureList: FeatureItem[] = [
  {
    title: 'Flask',
    Svg: require('@site/static/img/python2.svg').default,
    description: (
      <>
        Aquitectura de Microservicios, basada en Python, con principios de Clean Architecture: principios SOLID, TDD y DDD.
      </>
    ),
  },
  {
    title: 'Ecosistema GitHub',
    Svg: require('@site/static/img/github2.svg').default,
    description: (
      <>
        Repositorio privado, metodología ágil, estándares de calidad y prácticas DevSecOps.
      </>
    ),
  },
  {
    title: 'Cloud Native',
    Svg: require('@site/static/img/kubernetes.svg').default,
    description: (
      <>
        Ecosistema cloud con AWS y Kubernetes. Ambientes <i>Dev</i> y <i>QA</i>. Altos estándares de seguridad y monitoreo basados en RBAC, <a href='https://www.cisecurity.org/benchmark/kubernetes' target='_blank'>Normativas CIS</a>, networking e IAM Policies.
      </>
    ),
  },
];

function Feature({title, Svg, description}: FeatureItem) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures(): JSX.Element {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
