<?php

namespace App\Controller;

use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\Response;
use Symfony\Component\Routing\Annotation\Route;

class Accueil extends AbstractController
{
    #[Route('/nom/du', name: 'app_nom_du')]
    public function index(): Response
    {
        return $this->render('nom_du/index.html.twig', [
            'controller_name' => 'Accueil',
        ]);
    }
}
