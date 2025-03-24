interface Props {
    pageName: string;
    description: string;
  }
  
  const Breadcrumb = ({ pageName, description }: Props) => {
    return (
      <div className="py-8 text-center">
        <h1 className="text-3xl font-bold">{pageName}</h1>
        <p className="mt-2 text-gray-600">{description}</p>
      </div>
    );
  };
  
  export default Breadcrumb;
  